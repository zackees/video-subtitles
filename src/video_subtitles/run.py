"""
Runs the program
"""

import atexit
import concurrent.futures
import os
import shutil
from hashlib import md5

from appdirs import user_config_dir  # type: ignore
from disklru import DiskLRUCache  # type: ignore

from video_subtitles.convert_to_webvtt import convert_to_webvtt as convert_webvtt
from video_subtitles.translate import srt_wrap, translate
from video_subtitles.util import read_utf8

IS_GITHUB = os.environ.get("GITHUB_ACTIONS", False)
ALLOW_CONCURRENT_TRANSLATION = False

CACHE_FILE = os.path.join(user_config_dir("video-subtitles", "cache", roaming=True))

def find_srt_files(folder: str) -> list[str]:
    """Find srt files in a folder."""
    files = []
    # os walk
    for root, _, filenames in os.walk(folder):
        for filename in filenames:
            if filename.endswith(".srt"):
                files.append(os.path.join(root, filename))
    return files


def cleanup(file: str):
    """Attempts to remove the file."""
    if os.path.exists(file):
        try:
            os.remove(file)
        except Exception as err:  # pylint: disable=broad-except
            print(f"Error removing {file}: {err}")


def run(  # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    file: str,
    deepl_api_key: str | None,
    out_languages: list[str],
    model: str,
    convert_to_webvtt: bool,
) -> str:
    """Run the program."""
    from transcribe_anything.api import (  # pylint: disable=import-outside-toplevel
        transcribe,
    )
    cache = DiskLRUCache(CACHE_FILE, 16)
    file = os.path.abspath(file)
    print("Running transcription")
    out_languages = out_languages.copy()
    print(f"Output languages: {out_languages}")
    print(f"Model: {model}")
    print(f"File: {file}")
    print("Done running transcription")
    if deepl_api_key == "free":
        deepl_api_key = None
    device = "cuda" if not IS_GITHUB else "cpu"
    filemd5 = md5(file.encode("utf-8")).hexdigest()
    key = f"{file}-{filemd5}-{model}"
    cached_data = cache.get_json(key)
    if cached_data:
        print("Using cached data")
        out_en_dir = cached_data["out_en_dir"]
        os.makedirs(out_en_dir, exist_ok=True)
        srt_text = cached_data["srt_text"]
        if not os.path.exists(os.path.join(out_en_dir, "out.srt")):
            with open(os.path.join(out_en_dir, "out.srt"), "w", encoding="utf-8") as f:
                f.write(srt_text)
    else:
        out_en_dir = transcribe(url_or_file=file, device=device, model=model, language="en")
        out_en_dir = os.path.abspath(out_en_dir)
        srt_text = read_utf8(os.path.join(out_en_dir, "out.srt"))
        cache.put_json(key, {
            "out_en_dir": out_en_dir,
            "srt_text": srt_text
        })
    print(f"Output directory: {out_en_dir}")
    if not os.path.exists(out_en_dir):
        raise RuntimeError(f"Error - folder does not exist: {out_en_dir}")
    if "en" in out_languages:
        out_languages.remove("en")
    src_srt_file = os.path.join(out_en_dir, "out.srt")
    assert os.path.exists(src_srt_file), f"Error - file does not exist: {src_srt_file}"
    outdir = os.path.dirname(out_en_dir)
    tasks: list = []
    for language in out_languages:

        def do_translation(language: str = language):
            print(f"Translating to: {language}")
            out_folder = os.path.join(outdir, language)
            os.makedirs(out_folder, exist_ok=True)
            out_file = os.path.join(out_folder, "out.srt")
            attempts = 5
            for i in range(attempts):
                if i > 0:
                    print("Retrying...")
                try:
                    if os.path.exists(out_file):
                        os.remove(out_file)
                    translate(
                        api_key=deepl_api_key,
                        in_srt=src_srt_file,
                        out_srt=out_file,
                        from_lang="EN",
                        to_lang=language.upper(),
                    )
                    assert os.path.exists(
                        out_file
                    ), f"Error during translation of {language}: file does not exist: {out_file}"
                    break
                except Exception as err:  # pylint: disable=broad-except
                    print(err)
                    if i == attempts - 1:
                        raise
            print(f"Translated: {src_srt_file} -> {out_file}")

        tasks.append(do_translation)
    if not ALLOW_CONCURRENT_TRANSLATION or deepl_api_key is not None:
        # This is super fast so just run all the tasks one at a time
        for task in tasks:
            task()
    else:
        # Free api version uses selenium and is slow so run in parallel.
        print(
            "Free version of translation api is slow, so translating in parallel: "
            f"{len(tasks)} tasks"
        )
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            try:
                executor.map(lambda x: x(), tasks)
            except KeyboardInterrupt:
                print("Keyboard interrupt detected, exiting...")
                executor.shutdown(wait=False, cancel_futures=True)
    srt_wrap(src_srt_file)
    srt_files = find_srt_files(outdir)
    print(f"Found {len(srt_files)} srt files")
    for srt_file in srt_files:
        language_name = os.path.basename(os.path.dirname(srt_file))
        out_file = os.path.join(outdir, f"{language_name}.srt")
        if os.path.exists(out_file):
            os.remove(out_file)
        shutil.move(srt_file, out_file)
        shutil.rmtree(os.path.dirname(srt_file))
    if convert_to_webvtt:
        srt_files = find_srt_files(outdir)
        for srt_file in srt_files:
            webvtt_file = os.path.splitext(srt_file)[0] + ".vtt"
            if os.path.exists(webvtt_file):
                os.remove(webvtt_file)
            convert_webvtt(srt_file, webvtt_file)
            os.remove(srt_file)
    atexit.register(cleanup, os.path.abspath("geckodriver.log"))
    print("########################\n# Done translating!\n########################\n")
    return outdir

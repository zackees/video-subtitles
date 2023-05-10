"""
Runs the program
"""

import atexit
import os
import shutil

from video_subtitles.convert_to_webvtt import convert_to_webvtt as convert_webvtt
from video_subtitles.translate import srt_wrap, translate

IS_GITHUB = os.environ.get("GITHUB_ACTIONS", False)


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

    print("Running transcription")
    out_languages = out_languages.copy()
    print(f"Output languages: {out_languages}")
    print(f"Model: {model}")
    print(f"File: {file}")
    print("Done running transcription")
    if deepl_api_key == "free":
        deepl_api_key = None
    device = "cuda" if not IS_GITHUB else "cpu"
    out_en_dir = transcribe(url_or_file=file, device=device, model=model, language="en")
    print(f"Output directory: {out_en_dir}")
    if not os.path.exists(out_en_dir):
        raise RuntimeError(f"Error - folder does not exist: {out_en_dir}")
    if "en" in out_languages:
        out_languages.remove("en")
    src_srt_file = os.path.join(out_en_dir, "out.srt")
    assert os.path.exists(src_srt_file), f"Error - file does not exist: {src_srt_file}"
    outdir = os.path.dirname(out_en_dir)
    for language in out_languages:
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
                    from_lang="en",
                    to_lang=language,
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
    print("Done translating")
    return outdir

"""
Runs the program
"""
import os
import shutil

from transcribe_anything.api import transcribe

from video_subtitles.translate import srt_wrap, translate


def find_srt_files(folder: str) -> list[str]:
    """Find srt files in a folder."""
    files = []
    # os walk
    for root, _, filenames in os.walk(folder):
        for filename in filenames:
            if filename.endswith(".srt"):
                files.append(os.path.join(root, filename))
    return files


def run(  # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    file: str,
    out_languages: list[str],
    model: str,
) -> None:
    """Run the program."""
    print("Running transcription")
    out_languages = out_languages.copy()
    print(f"Output languages: {out_languages}")
    print(f"Model: {model}")
    print(f"File: {file}")
    print("Done running transcription")
    out_en_dir = transcribe(url_or_file=file, device="cuda", model=model, language="en")
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
        translate(src_srt_file, out_file, "en", language)
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
    print("Done translating")

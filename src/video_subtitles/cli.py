"""
Command line front end interface.
"""

import argparse
import os
import sys

from video_subtitles import __version__
from video_subtitles.run import run
from video_subtitles.util import (
    LANGUAGE_CODES,
    MODELS,
    GraphicsInfo,
    ensure_transcribe_anything_installed,
    query_cuda_video_cards,
)


def parse_languages(languages_str: str) -> list[str]:
    """Parse a comma-separated list of languages and return a list of language codes."""
    languages = languages_str.split(",")
    for language in languages:
        if language not in LANGUAGE_CODES:
            raise argparse.ArgumentTypeError(f"Invalid language code: {language}")
    return languages


def ensure_dependencies() -> list[GraphicsInfo]:
    """Ensure that dependencies are installed."""
    cuda_cards = query_cuda_video_cards()
    if not cuda_cards:
        raise RuntimeError("No Nvidia/CUDA video cards found.")
    ensure_transcribe_anything_installed()
    return cuda_cards


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    languages = LANGUAGE_CODES.keys()
    parser = argparse.ArgumentParser(description="Video Subtitles")
    parser.add_argument("--version", action="version", version=f"{__version__}")
    parser.add_argument("file", type=str, help="File or URL to process.")
    parser.add_argument(
        "--input-language",
        type=str,
        help="Input language.",
        choices=languages,
        default="en",
    )
    parser.add_argument(
        "--out-language",
        type=parse_languages,
        help="Output languages as a comma-separated list.",
        metavar="{en,es,fr,de,it,pt,ru,zh}",
        required=True,
    )
    parser.add_argument(
        "--model",
        type=str,
        help="Model to use.",
        default="medium",
        choices=MODELS.keys(),
    )
    args = parser.parse_args()
    if not args.out_language:
        parser.error("You must provide at least one --out-language")
    return args


def main() -> int:
    """Main entry point for the template_python_cmd package."""
    try:
        args = parse_args()
        file = args.file
        if not os.path.exists(file):
            print(f"Error - file does not exist: {file}")
            return 1
        print(f"videosubtitles version: {__version__}")
        cuda_cards = ensure_dependencies()
        print("Found the following Nvidia/CUDA video cards:")
        for card in cuda_cards:
            print(f"  [{card.idx}]: {card.name}, {card.memory_gb} GB")
        run(
            cuda_cards=cuda_cards,
            file=file,
            input_language=args.input_language,
            out_languages=args.out_language,
            model=args.model,
        )
    except KeyboardInterrupt:
        print("Exiting due to keyboard interrupt.")
        return 1
    return 0


if __name__ == "__main__":
    if True:  # pylint: disable=using-constant-test
        raise SystemExit(main())
    sys.argv.append("video.mp4")
    sys.argv.append("--out-language")
    sys.argv.append("en,es")
    sys.argv.append("--model")
    sys.argv.append("medium")
    main()

"""
Command line front end interface.
"""

import argparse
import os

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
    parser = argparse.ArgumentParser(description="Video Subtitles")
    parser.add_argument("--version", action="version", version=f"{__version__}")
    parser.add_argument("file", type=str, help="File or URL to process.")
    parser.add_argument(
        "--languages",
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
    if not args.languages:
        parser.error("You must provide at least one --languages")
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
            file=file,
            out_languages=args.languages,
            model=args.model,
        )
    except KeyboardInterrupt:
        print("Exiting due to keyboard interrupt.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

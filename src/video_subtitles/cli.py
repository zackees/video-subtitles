"""
Main entry point.
"""

from video_subtitles.util import (
    ensure_transcribe_anything_installed,
    query_cuda_video_cards,
)


def main() -> int:
    """Main entry point for the template_python_cmd package."""
    cuda_cards = query_cuda_video_cards()
    if not cuda_cards:
        print("No Nvidia/CUDA video cards found.")
        return 1
    print("Found the following Nvidia/CUDA video cards:")
    for card in cuda_cards:
        print(f"  {card.name}, {card.memory}")
    ensure_transcribe_anything_installed()
    print("Replace with a CLI entry point.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

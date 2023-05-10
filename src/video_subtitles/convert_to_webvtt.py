"""
Conversion to test to webvtt format.
"""


import webvtt  # pylint: disable=import-error


def convert_to_webvtt(srt_file: str, out_webvtt_file: str) -> None:
    """Convert to webvtt format."""
    assert srt_file.endswith(".srt")
    assert out_webvtt_file.endswith(".vtt")
    webvtt.from_srt(srt_file).save(out_webvtt_file)

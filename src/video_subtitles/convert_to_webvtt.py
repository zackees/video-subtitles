"""
Conversion to test to webvtt format.
"""


import webvtt  # pylint: disable=import-error

from video_subtitles.util import read_utf8, write_utf8

STYLE_ELEMENT = """STYLE
::::cue {
  line: 80%;
}

"""


def convert_to_webvtt(srt_file: str, out_webvtt_file: str) -> None:
    """Convert to webvtt format."""
    assert srt_file.endswith(".srt")
    assert out_webvtt_file.endswith(".vtt")
    webvtt.from_srt(srt_file).save(out_webvtt_file)
    content = read_utf8(out_webvtt_file)
    content = content.replace("WEBVTT\n\n", f"WEBVTT\n\n{STYLE_ELEMENT}")
    write_utf8(out_webvtt_file, content)

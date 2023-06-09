"""
Unit test file.
"""
import os
import tempfile
import unittest

from video_subtitles.convert_to_webvtt import convert_to_webvtt
from video_subtitles.util import read_utf8

HERE = os.path.dirname(os.path.abspath(__file__))

TEST_SRT = os.path.join(HERE, "test.srt")


class SrtToWebvtt(unittest.TestCase):
    """Main tester class."""

    def test_translate(self) -> None:
        """Test command line interface (CLI)."""
        # translator =  DeeplTranslator()  # free version
        with tempfile.TemporaryDirectory() as tmpdirname:
            out_file = os.path.join(tmpdirname, "out.vtt")
            convert_to_webvtt(TEST_SRT, out_file)
            content = read_utf8(out_file)
            print(content)


if __name__ == "__main__":
    unittest.main()

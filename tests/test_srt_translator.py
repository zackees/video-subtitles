"""
Unit test file.
"""
import os
import tempfile
import unittest

from video_subtitles.translate import translate

HERE = os.path.dirname(os.path.abspath(__file__))

SRT_TEXT = """
1
00:00:00,000 --> 00:00:08,700
Around the same time that John D. Rockefeller seized U.S. media, he also hijacked U.S. medicine.

2
00:00:08,700 --> 00:00:12,440
When it was discovered that drugs could be produced from petroleum, America's top oil

3
00:00:12,440 --> 00:00:17,880
mogul ordered his army of propagandists to invert reality accordingly.
"""

SRT_FILE = os.path.join(HERE, "out.srt")


class DeepLTester(unittest.TestCase):
    """Main tester class."""

    def test_translate(self) -> None:
        """Test command line interface (CLI)."""
        # translator =  DeeplTranslator()  # free version
        with tempfile.TemporaryDirectory() as tmpdirname:
            srt_file = os.path.join(tmpdirname, "in.srt")
            with open(srt_file, encoding="utf-8", mode="w") as f:
                f.write(SRT_TEXT)
            out_file = os.path.join(tmpdirname, "out.srt")
            translate(
                api_key=None,
                in_srt=srt_file,
                out_srt=out_file,
                from_lang="en",
                to_lang="es",
            )
            with open(out_file, encoding="utf-8", mode="r") as f:
                text = f.read()
        print(text)


if __name__ == "__main__":
    unittest.main()

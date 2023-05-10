"""
Unit test file.
"""
import os
import tempfile
import unittest

import webvtt

HERE = os.path.dirname(os.path.abspath(__file__))


TEST_SRT = os.path.join(HERE, "test.srt")


class SrtToWebvtt(unittest.TestCase):
    """Main tester class."""

    def test_translate(self) -> None:
        """Test command line interface (CLI)."""
        # translator =  DeeplTranslator()  # free version
        with tempfile.TemporaryDirectory() as tmpdirname:
            out_file = os.path.join(tmpdirname, "out.vtt")
            webvtt.from_srt(TEST_SRT).save(out_file)


if __name__ == "__main__":
    unittest.main()

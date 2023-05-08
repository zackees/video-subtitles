"""
Unit test file.
"""

import os
import shutil
import sys
import unittest

from video_subtitles.cli import main

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)


class MainTester(unittest.TestCase):
    """Main tester class."""

    def test_imports(self) -> None:
        """Test command line interface (CLI)."""
        shutil.rmtree("text_video", ignore_errors=True)
        sys.argv.append("video.mp4")
        sys.argv.append("--languages")
        sys.argv.append("es,fr,zh")
        sys.argv.append("--model")
        sys.argv.append("large")
        main()
        self.assertTrue(os.path.exists("text_video"))
        self.assertTrue(os.path.exists(os.path.join("text_video", "en.srt")))
        self.assertTrue(os.path.exists(os.path.join("text_video", "es.srt")))
        self.assertTrue(os.path.exists(os.path.join("text_video", "fr.srt")))
        self.assertTrue(os.path.exists(os.path.join("text_video", "zh.srt")))


if __name__ == "__main__":
    unittest.main()

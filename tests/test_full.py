"""
Unit test file.
"""

import os
import shutil
import unittest

from video_subtitles.run import run

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)


class MainTester(unittest.TestCase):
    """Main tester class."""

    def test_imports(self) -> None:
        """Test command line interface (CLI)."""
        shutil.rmtree("text_video", ignore_errors=True)
        run(
            file="video.mp4",
            deepl_api_key=None,
            out_languages=["es", "fr", "zh"],
            model="small",
        )
        self.assertTrue(os.path.exists("text_video"))
        self.assertTrue(os.path.exists(os.path.join("text_video", "en.srt")))
        self.assertTrue(os.path.exists(os.path.join("text_video", "es.srt")))
        self.assertTrue(os.path.exists(os.path.join("text_video", "fr.srt")))
        self.assertTrue(os.path.exists(os.path.join("text_video", "zh.srt")))


if __name__ == "__main__":
    unittest.main()

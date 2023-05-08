"""
Unit test file.
"""
import os
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

COMMAND = "videosubtitles video.mp4 --api-key free --languages es,fr,zh --model large"


class MainTester(unittest.TestCase):
    """Main tester class."""

    def test_imports(self) -> None:
        """Test command line interface (CLI)."""
        rtn = os.system(COMMAND)
        self.assertEqual(0, rtn)


if __name__ == "__main__":
    unittest.main()

"""
Unit test file.
"""
import os
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

COMMAND = "videosubtitles video.mp4 --api-key free --languages es,fr,zh --model large"

IS_GITHUB = os.environ.get("GITHUB_ACTIONS", False)

class MainTester(unittest.TestCase):
    """Main tester class."""

    @unittest.skipIf(IS_GITHUB, "Skip if running on GitHub Actions.")
    def test_imports(self) -> None:
        """Test command line interface (CLI)."""
        rtn = os.system(COMMAND)
        self.assertEqual(0, rtn)


if __name__ == "__main__":
    unittest.main()

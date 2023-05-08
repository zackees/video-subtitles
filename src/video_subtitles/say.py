"""
Text to speech.
"""

import os
from tempfile import NamedTemporaryFile
from typing import Optional

from gtts import gTTS  # type: ignore
from playaudio import playaudio  # type: ignore

IS_GITHUB = os.environ.get("GITHUB_ACTIONS", False)


def say(text: str, output: Optional[str] = None) -> None:
    """Say something."""
    if IS_GITHUB:
        return
    tempmp3 = NamedTemporaryFile(  # pylint: disable=consider-using-with
        suffix=".mp3", delete=False
    )
    tempmp3.close()
    try:
        tts = gTTS(text=text, lang="en")
        if output:
            tts.save(output)
            return
        tts.save(tempmp3.name)
        playaudio(tempmp3.name)
    finally:
        os.remove(tempmp3.name)

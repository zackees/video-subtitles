"""
Reads and writes settings to a json file.
"""

import json
import os

from appdirs import user_config_dir  # type: ignore

HERE = os.path.dirname(os.path.abspath(__file__))


def get_settings_path() -> str:
    """Get settings path"""
    env_path = user_config_dir("video-subtitles", "video-subtitles", roaming=True)
    config_file = os.path.join(env_path, "settings.json")
    os.makedirs(env_path, exist_ok=True)
    return config_file


SETTINGS_JSON = get_settings_path()


class Settings:
    """Settings class."""

    def __init__(self) -> None:
        self.data: dict[str, str | int | dict | list] = {}
        self.load()

    def deepl_key(self) -> str | None:
        """Return the DeepL API key."""
        return self.data.get("deepl_key", None)  # type: ignore

    def set_deepl_key(self, key: str) -> None:
        """Set the DeepL API key."""
        self.data["deepl_key"] = key

    def model(self) -> str:
        """Return the model."""
        return self.data.get("model", "large")  # type: ignore

    def set_model(self, model: str) -> None:
        """Set the model."""
        self.data["model"] = model

    def languages(self) -> list[str]:
        """Return the languages."""
        out = self.data.get(
            "languages", ["en", "es", "fr", "de", "it", "pt", "ru", "zh"]
        )
        return out  # type: ignore

    def set_languages(self, languages: list[str]) -> None:
        """Set the languages."""
        self.data["languages"] = languages

    def subtitle_format(self) -> str:
        """Return the subtitle format."""
        return self.data.get("subtitle_format", "WEBVTT")  # type: ignore

    def set_subtitle_format(self, subtitle_format: str) -> None:
        """Set the subtitle format."""
        assert subtitle_format in ["WEBVTT", "SRT"]
        self.data["subtitle_format"] = subtitle_format

    def save(self) -> None:
        """Save the settings."""
        # dump json to file
        with open(SETTINGS_JSON, encoding="utf-8", mode="w") as f:
            json.dump(self.data, f, indent=4)

    def load(self) -> None:
        """Load the settings."""
        # load json from file
        if not os.path.exists(SETTINGS_JSON):
            self.data = {}
            return
        with open(SETTINGS_JSON, encoding="utf-8", mode="r") as f:
            self.data = json.load(f)

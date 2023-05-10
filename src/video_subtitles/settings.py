"""
Reads and writes settings to a json file.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

SETTINGS_JSON = os.path.join(HERE, "settings.json")


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

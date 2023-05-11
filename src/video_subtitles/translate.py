"""
Handles srt translation and wrapping.
"""

# pylint: disable=import-error

from srtranslator import SrtFile
from srtranslator.translators.deepl_api import DeeplApi
from srtranslator.translators.deepl_scrap import DeeplTranslator as FreeTranslator
from srtranslator.translators.translatepy import TranslatePy as GoogleTranslator


def srt_wrap(srt_file: str) -> None:
    """Wrap lines in a srt file."""
    srt = SrtFile(srt_file)
    srt.wrap_lines()
    srt.save(srt_file)


def convert_deepl_language_codes_to_google(lang: str) -> str:
    """Some Google language codes are different from Deepl's, non-exhaustive list."""
    if "PT-" in lang:  # Portuguese dialects not supported by google.
        lang = "PT"
    if "NB" in lang:
        lang = "NO"
    return lang.lower()


def translate(
    api_key: str | None, in_srt: str, out_srt: str, from_lang: str, to_lang: str
) -> None:
    """Translate a srt file."""
    if api_key is None:
        translator = FreeTranslator()
        from_lang = from_lang.lower()
        to_lang = to_lang.lower()
    elif api_key.lower() == "google":
        from_lang = convert_deepl_language_codes_to_google(from_lang)
        to_lang = convert_deepl_language_codes_to_google(to_lang)
        translator = GoogleTranslator()
    else:
        from_lang = from_lang.lower()
        to_lang = to_lang.lower()
        translator = DeeplApi(api_key=api_key)
    srt = SrtFile(in_srt)
    srt.translate(translator, from_lang, to_lang)
    srt.wrap_lines()
    srt.save(out_srt)

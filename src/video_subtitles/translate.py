"""
Handles srt translation and wrapping.
"""

# pylint: disable=import-error

from srtranslator import SrtFile
from srtranslator.translators.deepl_api import DeeplApi
from srtranslator.translators.deepl_scrap import DeeplTranslator as FreeTranslator
# from srtranslator.translators.translatepy import TranslatePy


def srt_wrap(srt_file: str) -> None:
    """Wrap lines in a srt file."""
    srt = SrtFile(srt_file)
    srt.wrap_lines()
    srt.save(srt_file)


def translate(api_key: str | None, in_srt: str, out_srt: str, from_lang: str, to_lang: str) -> None:
    """Translate a srt file."""
    if api_key is None:
        translator = FreeTranslator()
    else:
        translator = DeeplApi(api_key=api_key)
    srt = SrtFile(in_srt)
    srt.translate(translator, from_lang, to_lang)
    srt.wrap_lines()
    srt.save(out_srt)

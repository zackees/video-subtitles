"""
Handles srt translation and wrapping.
"""

# pylint: disable=import-error

from srtranslator import SrtFile
from srtranslator.translators.deepl_api import DeeplApi

# from srtranslator.translators.deepl_scrap import DeeplTranslator
# from srtranslator.translators.translatepy import TranslatePy

API_KEY = "529e9048-162e-6ebc-c56f-9a869afd2d85:fx"


def srt_wrap(srt_file: str) -> None:
    """Wrap lines in a srt file."""
    srt = SrtFile(srt_file)
    srt.wrap_lines()
    srt.save(srt_file)


def translate(in_srt: str, out_srt: str, from_lang: str, to_lang: str) -> None:
    """Translate a srt file."""
    translator = DeeplApi(api_key=API_KEY)
    srt = SrtFile(in_srt)
    srt.translate(translator, from_lang, to_lang)
    srt.wrap_lines()
    srt.save(out_srt)

"""Utilities for video_subtitles."""

import os
import subprocess
import tempfile
from dataclasses import dataclass
from shutil import which

from download import download  # type: ignore

INSTALL_TRANSCRIBE_ANYTHING_CUDA = (
    "https://raw.githubusercontent.com/zackees/transcribe-anything/main/install_cuda.py"
)


@dataclass
class GraphicsInfo:
    """Graphics card information."""

    name: str
    memory_gb: float
    idx: int


def read_utf8(path: str) -> str:
    """Read a UTF-8 file."""
    with open(path, encoding="utf-8", mode="r") as file:
        return file.read()


def write_utf8(path: str, text: str) -> None:
    """Write a UTF-8 file."""
    with open(path, encoding="utf-8", mode="w") as file:
        file.write(text)


def query_cuda_video_cards() -> list[GraphicsInfo]:
    """Query the video cards on the system."""
    print("Querying video cards...")
    if which("nvidia-smi") is None:
        raise RuntimeError("nvidia-smi is not installed.")
    cmd = "nvidia-smi --query-gpu=name,memory.total --format=csv,noheader"
    text = subprocess.check_output(cmd.split(" "), universal_newlines=True)
    lines = [line.strip() for line in text.split("\n") if line.strip() != ""]
    out: list[GraphicsInfo] = []
    for i, line in enumerate(lines):
        name, memory = line.split(",")
        memory_gb = int(memory.strip().split(" ")[0]) / 1024.0
        out.append(GraphicsInfo(name, memory_gb, i))
    return out


def ensure_transcribe_anything_installed() -> None:
    """Ensure that transcribe_anything is installed."""
    print("Checking that transcribe_anything is installed...")
    try:
        subprocess.check_output(["transcribe_anything", "--help"])
        print("...it is.")
        return
    except Exception:  # pylint: disable=broad-except
        print("transcribe_anything is not installed, installing now...")
        with tempfile.TemporaryDirectory() as tempdir:
            download(
                INSTALL_TRANSCRIBE_ANYTHING_CUDA,
                os.path.join(tempdir, "install_cuda.py"),
            )
            rtn = subprocess.call(["python", os.path.join(tempdir, "install_cuda.py")])
            if rtn != 0:
                raise RuntimeError(  # pylint: disable=raise-missing-from
                    "install_cuda.py failed."
                )


LANGUAGE_CODES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "zh": "Chinese",
}

MODELS = {
    # Maps model name to number of GPU memory (in gigabytes) required.
    "tiny": 1.0,
    "base": 1.0,
    "small": 2.0,
    "medium": 5.0,
    "large": 10.0,
}

"""Utilities for video_subtitles."""

import os
import subprocess
import tempfile
from dataclasses import dataclass
from shutil import which

from download import download  # type: ignore

URL = (
    "https://raw.githubusercontent.com/zackees/transcribe-anything/main/install_cuda.py"
)


@dataclass
class GraphicsInfo:
    """Graphics card information."""

    name: str
    memory: str


def query_cuda_video_cards() -> list[GraphicsInfo]:
    """Query the video cards on the system."""
    print("Querying video cards...")
    if which("nvidia-smi") is None:
        raise RuntimeError("nvidia-smi is not installed.")
    cmd = "nvidia-smi --query-gpu=name,memory.total --format=csv,noheader"
    text = subprocess.check_output(cmd.split(" "), universal_newlines=True)
    lines = [line.strip() for line in text.split("\n") if line.strip() != ""]
    out: list[GraphicsInfo] = []
    for line in lines:
        name, memory = line.split(",")
        memory = memory.strip()
        out.append(GraphicsInfo(name, memory))
    return out


def ensure_transcribe_anything_installed() -> None:
    """Ensure that transcribe_anything is installed."""
    print("Checking that transcribe_anything is installed...")
    try:
        subprocess.check_output(["transcribe_anything", "--help"])
        return
    except subprocess.CalledProcessError:
        print("transcribe_anything is not installed, installing now...")
        with tempfile.TemporaryDirectory() as tempdir:
            download(URL, os.path.join(tempdir, "install_cuda.py"))
            rtn = subprocess.call(["python", os.path.join(tempdir, "install_cuda.py")])
            if rtn != 0:
                raise RuntimeError(  # pylint: disable=raise-missing-from
                    "install_cuda.py failed."
                )

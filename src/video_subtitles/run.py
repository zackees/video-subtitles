"""
Runs the program
"""

import subprocess
import time
from dataclasses import dataclass

from video_subtitles.util import MODELS, GraphicsInfo


@dataclass
class ProcessingJob:
    """Graphics card information."""

    cmd: str
    model: str
    running_proc: subprocess.Popen | None = None
    cuda_card: GraphicsInfo | None = None
    rtn_value: int | None = None


def get_next_available_card(
    available_cuda_cards: list[GraphicsInfo], job: ProcessingJob
) -> GraphicsInfo | None:
    """Get the next job to run."""
    model_size_gb = MODELS[job.model]
    for card in available_cuda_cards:
        if card.memory_gb >= model_size_gb:
            return card
    return None


def generate_cmd(file: str, input_language: str, out_language: str, model: str) -> str:
    """Generate the command to run."""
    task = "transcribe" if out_language == "en" else "translate"
    return f"echo {file}, using {model} to {task}: {input_language} -> {out_language}"


def run(  # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    cuda_cards: list[GraphicsInfo],
    file: str,
    input_language: str,
    out_languages: list[str],
    model: str,
) -> None:
    """Run the program."""
    print("Running transcription")
    out_languages = out_languages.copy()
    print(f"Input language: {input_language}")
    print(f"Output languages: {out_languages}")
    print(f"Model: {model}")
    print(f"File: {file}")
    print(f"CUDA cards: {cuda_cards}")
    print("Done running transcription")
    available_cuda_cards = cuda_cards.copy()
    # cmd = [
    #   "transcribe-anything", "--cuda", str(card.idx), "--model", model, "--input-language",
    #   input_language, "--out-language", out_languages.pop(0), file]
    # check that all jobs can run on available cards
    pending_jobs: list[ProcessingJob] = []
    for out_language in out_languages:
        cmd = generate_cmd(
            file=file,
            input_language=input_language,
            out_language=out_language,
            model=model,
        )
        job = ProcessingJob(cmd=cmd, model=model)
        pending_jobs.append(job)
    for job in pending_jobs:
        card = get_next_available_card(available_cuda_cards, job)
        if card is None:
            raise RuntimeError("Not enough GPU memory to run all jobs.")
    max_jobs = len(cuda_cards)
    running_jobs: list[ProcessingJob] = []
    finished_jobs: list[ProcessingJob] = []
    while True:
        # Check if any jobs have finished.
        for job in running_jobs.copy():
            assert job.running_proc is not None
            assert job.cuda_card is not None
            rtn = job.running_proc.poll()
            if rtn is not None:
                cmd = job.cmd
                if rtn != 0:
                    error_str = (
                        f"Error - job on card {job.cuda_card.idx} "
                        f"failed with return code {rtn}, while running command: {cmd}"
                    )
                    print(error_str)
                else:
                    print(f"Job on card {job.cuda_card.idx} finished successfully.")
                job.rtn_value = rtn
                finished_jobs.append(job)
                available_cuda_cards.append(job.cuda_card)
                running_jobs.remove(job)
        if len(running_jobs) >= max_jobs:
            time.sleep(0.25)
            continue
        queued_new_job = False
        for job in pending_jobs.copy():
            # Get the next job to run.
            card = get_next_available_card(available_cuda_cards, job)
            if card is None:
                continue
            # Run the job.
            cmd = job.cmd
            print(f"Running command: {cmd}")
            proc = subprocess.Popen(  # pylint: disable=consider-using-with
                cmd.split(" ")
            )
            job.running_proc = proc
            job.cuda_card = card
            queued_new_job = True
            running_jobs.append(job)
            available_cuda_cards.remove(card)
            pending_jobs.remove(job)
            break
        if queued_new_job:
            continue
        # now check if no jobs can be started
        if len(running_jobs) == 0 and len(pending_jobs) > 0:
            raise RuntimeError("Not enough GPU memory to run all jobs.")
        if len(running_jobs) == 0 and len(pending_jobs) == 0:
            break  # Done
    one_or_more_errors = False
    for job in finished_jobs:
        rtn = job.rtn_value
        cmd = job.cmd
        assert job.cuda_card is not None
        if rtn != 0:
            error_str = (
                f"Error - job {cmd} on card {job.cuda_card.idx} failed with return code {rtn}"
                f", while running command: {cmd}"
            )
            print(error_str)
            one_or_more_errors = True
    if one_or_more_errors:
        raise RuntimeError("One or more jobs failed.")
    print("All jobs finished successfully.")

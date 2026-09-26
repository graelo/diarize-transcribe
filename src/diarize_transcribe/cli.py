"""Typer command-line interface."""

from __future__ import annotations

import platform
from pathlib import Path
from typing import Annotated

import typer

from diarize_transcribe import __version__
from diarize_transcribe.models import DEFAULT_ASR_LANGUAGE
from diarize_transcribe.pipeline import ModelError, run_transcription
from diarize_transcribe.transcript import (
    DEFAULT_SPEAKER_GAP_SECONDS,
    validate_speaker_gap_seconds,
    write_transcript,
)

app = typer.Typer(
    name="diarize-transcribe",
    help="Transcribe an audio file with speaker diarization.",
    no_args_is_help=True,
    add_completion=False,
)


def _version_callback(value: bool) -> bool:
    if value:
        typer.echo(__version__)
        raise typer.Exit()
    return value


def _supported_platform() -> bool:
    return platform.system() == "Darwin" and platform.machine() in {"arm64", "aarch64"}


def _speaker_gap_callback(value: float) -> float:
    try:
        return validate_speaker_gap_seconds(value)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc


@app.command()
def run(
    audio: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            help="Input audio file.",
        ),
    ],
    output: Annotated[
        Path,
        typer.Option("--output", "-o", help="Output transcript text file."),
    ],
    language: Annotated[
        str,
        typer.Option(
            "--language",
            help="ASR language prompt key.",
            show_default=True,
        ),
    ] = DEFAULT_ASR_LANGUAGE,
    speaker_gap_seconds: Annotated[
        float,
        typer.Option(
            "--speaker-gap-seconds",
            callback=_speaker_gap_callback,
            help="Merge same-speaker turns separated by less than this many seconds.",
            show_default=True,
        ),
    ] = DEFAULT_SPEAKER_GAP_SECONDS,
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            callback=_version_callback,
            is_eager=True,
            help="Show the installed version and exit.",
        ),
    ] = False,
) -> None:
    """Diarize and transcribe one audio file into speaker turns."""
    del version

    if not _supported_platform():
        typer.echo(
            "Error: local MLX inference requires macOS on Apple Silicon.",
            err=True,
        )
        raise typer.Exit(code=1)

    if output.resolve() == audio.resolve():
        raise typer.BadParameter("output must not overwrite the input audio file")
    if output.exists() and not output.is_file():
        raise typer.BadParameter("output must be a file path, not a directory")
    if not output.parent.exists() or not output.parent.is_dir():
        raise typer.BadParameter("the output parent directory must already exist")

    try:
        lines = run_transcription(
            audio, language=language, speaker_gap_seconds=speaker_gap_seconds
        )
        write_transcript(output, lines)
    except ModelError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1) from exc
    except OSError as exc:
        typer.echo(f"Error writing transcript: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    typer.echo(f"Transcript written to {output}")


if __name__ == "__main__":
    app()

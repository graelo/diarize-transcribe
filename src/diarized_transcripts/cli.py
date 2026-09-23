"""Typer command-line interface."""

from __future__ import annotations

import platform
from pathlib import Path
from typing import Annotated

import typer

from diarized_transcripts import __version__
from diarized_transcripts.pipeline import ModelError, run_transcription
from diarized_transcripts.transcript import write_transcript

app = typer.Typer(
    name="diarize",
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
        lines = run_transcription(audio)
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

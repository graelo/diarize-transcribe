"""Coordinate diarization, speech recognition, and transcript formatting."""

from __future__ import annotations

from pathlib import Path

from diarize_transcribe.models import (
    DEFAULT_ASR_LANGUAGE,
    ModelError,
    diarize_audio,
    transcribe_audio,
)
from diarize_transcribe.transcript import render_lines

__all__ = ["ModelError", "run_transcription"]


def run_transcription(
    audio: Path, language: str = DEFAULT_ASR_LANGUAGE
) -> list[str]:
    """Run the fixed model pair and return formatted speaker-turn lines."""
    turns = diarize_audio(audio)
    segments = transcribe_audio(audio, language=language)
    return render_lines(turns, segments)

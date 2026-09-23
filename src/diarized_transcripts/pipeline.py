"""Coordinate diarization, speech recognition, and transcript formatting."""

from __future__ import annotations

from pathlib import Path

from diarized_transcripts.models import ModelError, diarize_audio, transcribe_audio
from diarized_transcripts.transcript import render_lines

__all__ = ["ModelError", "run_transcription"]


def run_transcription(audio: Path) -> list[str]:
    """Run the fixed model pair and return formatted speaker-turn lines."""
    turns = diarize_audio(audio)
    segments = transcribe_audio(audio)
    return render_lines(turns, segments)

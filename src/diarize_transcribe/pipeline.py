"""Coordinate diarization, speech recognition, and transcript formatting."""

from __future__ import annotations

from pathlib import Path

from diarize_transcribe.models import (
    DEFAULT_ASR_LANGUAGE,
    ModelError,
    diarize_audio,
    transcribe_audio,
)
from diarize_transcribe.transcript import (
    DEFAULT_SPEAKER_GAP_SECONDS,
    render_lines,
    validate_speaker_gap_seconds,
)

__all__ = ["ModelError", "run_transcription"]


def run_transcription(
    audio: Path,
    language: str = DEFAULT_ASR_LANGUAGE,
    speaker_gap_seconds: float = DEFAULT_SPEAKER_GAP_SECONDS,
) -> list[str]:
    """Run the fixed model pair and return formatted speaker-turn lines."""
    validate_speaker_gap_seconds(speaker_gap_seconds)
    turns = diarize_audio(audio)
    segments = transcribe_audio(audio, language=language)
    return render_lines(turns, segments, speaker_gap_seconds)

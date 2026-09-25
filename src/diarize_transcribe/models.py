"""Adapters for the pinned mlx-audio model APIs."""

from __future__ import annotations

from pathlib import Path

from diarize_transcribe.transcript import SpeakerTurn, TextSegment

DIARIZATION_MODEL = "mlx-community/Nemotron-3-Diarization"
ASR_MODEL = "animaslabs/parakeet-tdt-0.6b-v3-mlx-8bit"
DEFAULT_ASR_CHUNK_SECONDS = 300.0
ASR_CHUNK_OVERLAP_SECONDS = 2.0


class ModelError(RuntimeError):
    """A required model could not be loaded or run."""


def diarize_audio(audio: Path) -> list[SpeakerTurn]:
    try:
        from mlx_audio.vad import load

        model = load(DIARIZATION_MODEL, strict=True)
        result = model.generate(str(audio))
        return [
            SpeakerTurn(
                start=float(segment.start),
                end=float(segment.end),
                speaker=str(segment.speaker),
            )
            for segment in result.segments
        ]
    except Exception as exc:
        raise ModelError(f"Nemotron diarization failed ({DIARIZATION_MODEL}): {exc}") from exc


def transcribe_audio(
    audio: Path, chunk_seconds: float = DEFAULT_ASR_CHUNK_SECONDS
) -> list[TextSegment]:
    try:
        from mlx_audio.stt import load

        model = load(ASR_MODEL)
        result = model.generate(
            str(audio),
            chunk_duration=chunk_seconds,
            overlap_duration=ASR_CHUNK_OVERLAP_SECONDS,
        )
        return [
            TextSegment(
                start=float(sentence.start),
                end=float(sentence.end),
                text=str(sentence.text),
            )
            for sentence in result.sentences
        ]
    except Exception as exc:
        raise ModelError(f"Parakeet transcription failed ({ASR_MODEL}): {exc}") from exc

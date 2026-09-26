"""Adapters for the pinned mlx-audio model APIs."""

from __future__ import annotations

from pathlib import Path

from diarize_transcribe.transcript import SpeakerTurn, TimedTextToken

DIARIZATION_MODEL = "mlx-community/Nemotron-3-Diarization"
ASR_MODEL = "mlx-community/nemotron-3.5-asr-streaming-0.6b-8bit"
DEFAULT_ASR_LANGUAGE = "auto"


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
    audio: Path, language: str = DEFAULT_ASR_LANGUAGE
) -> list[TimedTextToken]:
    try:
        from mlx_audio.stt import load

        model = load(ASR_MODEL)
        prompt_dictionary = getattr(model, "prompt_dictionary", {})
        if language not in prompt_dictionary:
            supported = ", ".join(sorted(prompt_dictionary)) or "none"
            raise ValueError(
                f"unsupported language prompt {language!r}; "
                f"supported prompts: {supported}"
            )

        result = model.generate(str(audio), language=language)
        return sorted(
            (
                TimedTextToken(
                    start=float(token.start),
                    end=float(token.end),
                    text=str(token.text),
                )
                for sentence in result.sentences
                for token in sentence.tokens
            ),
            key=lambda token: token.start,
        )
    except Exception as exc:
        raise ModelError(f"Nemotron transcription failed ({ASR_MODEL}): {exc}") from exc

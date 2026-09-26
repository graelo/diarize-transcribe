from pathlib import Path

import pytest

from diarize_transcribe import pipeline
from diarize_transcribe.models import DEFAULT_ASR_LANGUAGE
from diarize_transcribe.transcript import SpeakerTurn, TimedTextToken


def test_run_transcription_forwards_language_and_preserves_global_times(
    monkeypatch, tmp_path: Path
) -> None:
    audio = tmp_path / "recording.wav"
    requested_languages: list[str] = []
    monkeypatch.setattr(
        pipeline,
        "diarize_audio",
        lambda path: [SpeakerTurn(300.0, 302.0, "speaker_0")],
    )

    def transcribe(path: Path, *, language: str = DEFAULT_ASR_LANGUAGE):
        requested_languages.append(language)
        return [TimedTextToken(300.2, 301.2, "Hello.")]

    monkeypatch.setattr(pipeline, "transcribe_audio", transcribe)

    rendered_thresholds: list[float] = []
    render_lines = pipeline.render_lines

    def capture_rendering(turns, tokens, speaker_gap_seconds: float):
        rendered_thresholds.append(speaker_gap_seconds)
        return render_lines(turns, tokens, speaker_gap_seconds)

    monkeypatch.setattr(pipeline, "render_lines", capture_rendering)

    result = pipeline.run_transcription(
        audio, language="test-language", speaker_gap_seconds=2.5
    )

    assert requested_languages == ["test-language"]
    assert rendered_thresholds == [2.5]
    assert result == ["[300.000:302.000] speaker-0 -- Hello."]


@pytest.mark.parametrize("speaker_gap_seconds", [-1.0, float("nan"), float("inf")])
def test_run_transcription_rejects_invalid_speaker_gap_before_inference(
    monkeypatch, tmp_path: Path, speaker_gap_seconds: float
) -> None:
    monkeypatch.setattr(
        pipeline,
        "diarize_audio",
        lambda path: (_ for _ in ()).throw(AssertionError("must not run")),
    )

    with pytest.raises(ValueError, match="finite and non-negative"):
        pipeline.run_transcription(
            tmp_path / "recording.wav", speaker_gap_seconds=speaker_gap_seconds
        )

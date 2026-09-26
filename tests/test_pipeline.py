from pathlib import Path

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

    result = pipeline.run_transcription(audio, language="test-language")

    assert requested_languages == ["test-language"]
    assert result == ["[300.000:302.000] speaker-0 -- Hello."]

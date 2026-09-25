from pathlib import Path

from diarize_transcribe import pipeline
from diarize_transcribe.models import DEFAULT_ASR_CHUNK_SECONDS
from diarize_transcribe.transcript import SpeakerTurn, TextSegment


def test_run_transcription_forwards_chunk_duration_and_preserves_global_times(
    monkeypatch, tmp_path: Path
) -> None:
    audio = tmp_path / "recording.wav"
    requested_durations: list[float] = []
    monkeypatch.setattr(
        pipeline,
        "diarize_audio",
        lambda path: [SpeakerTurn(300.0, 302.0, "speaker_0")],
    )

    def transcribe(path: Path, *, chunk_seconds: float = DEFAULT_ASR_CHUNK_SECONDS):
        requested_durations.append(chunk_seconds)
        return [TextSegment(300.2, 301.2, "Hello.")]

    monkeypatch.setattr(pipeline, "transcribe_audio", transcribe)

    result = pipeline.run_transcription(audio, chunk_seconds=120.0)

    assert requested_durations == [120.0]
    assert result == ["[300.000:302.000] speaker-0 -- Hello."]

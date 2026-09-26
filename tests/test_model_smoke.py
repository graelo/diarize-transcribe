import os
import re
from pathlib import Path

import pytest

from diarize_transcribe import pipeline
from diarize_transcribe.transcript import TimedTextToken

FIXTURE = Path(__file__).parent / "fixtures" / "two_speakers_15-20s.wav"
FIXTURE_SECONDS = 17.175
LINE_PATTERN = re.compile(r"\[(\d+\.\d{3}):(\d+\.\d{3})\] (speaker-\d+) -- (.+)\n?")


@pytest.mark.integration
@pytest.mark.skipif(
    os.environ.get("RUN_MODEL_SMOKE") != "1",
    reason="set RUN_MODEL_SMOKE=1 to download model weights and run the pipeline",
)
def test_transcribes_timed_tokens_for_two_speaker_fixture(monkeypatch) -> None:
    captured_tokens: list[TimedTextToken] = []
    transcribe_audio = pipeline.transcribe_audio

    def capture_tokens(audio: Path, *, language: str):
        tokens = transcribe_audio(audio, language=language)
        captured_tokens.extend(tokens)
        return tokens

    monkeypatch.setattr(pipeline, "transcribe_audio", capture_tokens)

    lines = pipeline.run_transcription(FIXTURE, language="auto")

    assert captured_tokens
    assert all(isinstance(token, TimedTextToken) for token in captured_tokens)
    assert captured_tokens == sorted(captured_tokens, key=lambda token: token.start)
    assert all(
        0.0 <= token.start < token.end <= FIXTURE_SECONDS + 1.0
        and token.text
        for token in captured_tokens
    )

    assert lines
    speakers: set[str] = set()
    for line in lines:
        match = LINE_PATTERN.fullmatch(line)
        assert match is not None, f"unexpected transcript line format: {line!r}"
        start, end, speaker, text = match.groups()
        assert 0.0 <= float(start) < float(end) <= FIXTURE_SECONDS + 1.0
        assert text.strip()
        speakers.add(speaker)

    assert len(speakers) >= 2

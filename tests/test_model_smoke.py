import os
import re
from pathlib import Path

import pytest

FIXTURE = Path(__file__).parent / "fixtures" / "two_speakers_15-20s.wav"
FIXTURE_SECONDS = 17.175
LINE_PATTERN = re.compile(r"\[(\d+\.\d{3}):(\d+\.\d{3})\] (speaker-\d+) -- (.+)\n?")


@pytest.mark.integration
@pytest.mark.skipif(
    os.environ.get("RUN_MODEL_SMOKE") != "1",
    reason="set RUN_MODEL_SMOKE=1 to download model weights and run the pipeline",
)
def test_transcribes_two_speaker_fixture_end_to_end() -> None:
    from diarize_transcribe.pipeline import run_transcription

    lines = run_transcription(FIXTURE, language="auto")

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

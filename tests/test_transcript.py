from pathlib import Path

from diarized_transcripts.transcript import (
    SpeakerTurn,
    TextSegment,
    align_text_to_turns,
    render_lines,
    write_transcript,
)


def test_assigns_text_to_turn_with_greatest_overlap_and_orders_text() -> None:
    turns = [SpeakerTurn(0, 2, "speaker_0"), SpeakerTurn(2, 4, "speaker_1")]
    segments = [
        TextSegment(2.2, 2.8, "second."),
        TextSegment(1.2, 2.4, "first."),
    ]

    assert align_text_to_turns(turns, segments) == [
        (turns[0], "first."),
        (turns[1], "second."),
    ]


def test_equal_overlap_uses_segment_midpoint_turn() -> None:
    turns = [SpeakerTurn(0, 2, "speaker_0"), SpeakerTurn(2, 4, "speaker_1")]
    segments = [TextSegment(1, 3, "boundary")]

    assert align_text_to_turns(turns, segments) == [(turns[1], "boundary")]


def test_omits_unassigned_empty_and_zero_duration_segments() -> None:
    turns = [SpeakerTurn(0, 1, "speaker_0"), SpeakerTurn(2, 3, "speaker_1")]
    segments = [
        TextSegment(1, 2, "in the gap"),
        TextSegment(0.2, 0.7, "  "),
        TextSegment(0.2, 0.2, "instant"),
    ]

    assert align_text_to_turns(turns, segments) == []
    assert render_lines(turns, segments) == []


def test_overlapping_turns_receive_separate_lines_by_best_overlap() -> None:
    turns = [SpeakerTurn(0, 2, "speaker_0"), SpeakerTurn(1, 3, "speaker_1")]
    segments = [TextSegment(0.2, 0.9, "one"), TextSegment(2.1, 2.8, "two")]

    assert render_lines(turns, segments) == [
        "[0.000:2.000] speaker_0 -- one",
        "[1.000:3.000] speaker_1 -- two",
    ]


def test_write_transcript_creates_utf8_file_with_newlines(tmp_path: Path) -> None:
    output = tmp_path / "transcript.txt"

    write_transcript(output, ["[0.000:1.000] speaker_0 -- café"])

    assert output.read_bytes() == "[0.000:1.000] speaker_0 -- café\n".encode()
    write_transcript(output, [])
    assert output.read_bytes() == b""

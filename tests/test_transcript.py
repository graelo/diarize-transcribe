from pathlib import Path

from diarize_transcribe.transcript import (
    SpeakerTurn,
    TimedTextToken,
    align_text_to_turns,
    coalesce_speaker_turns,
    render_lines,
    write_transcript,
)


def test_assigns_tokens_across_speaker_boundaries_and_orders_text() -> None:
    turns = [SpeakerTurn(0, 2, "speaker_0"), SpeakerTurn(2, 4, "speaker_1")]
    tokens = [
        TimedTextToken(2.2, 2.8, " second."),
        TimedTextToken(1.6, 1.9, " first"),
        TimedTextToken(1.2, 1.6, "The"),
    ]

    assert align_text_to_turns(turns, tokens) == [
        (turns[0], "The first"),
        (turns[1], "second."),
    ]


def test_equal_overlap_uses_token_midpoint_turn() -> None:
    turns = [SpeakerTurn(0, 2, "speaker_0"), SpeakerTurn(2, 4, "speaker_1")]
    tokens = [TimedTextToken(1, 3, "boundary")]

    assert align_text_to_turns(turns, tokens) == [(turns[1], "boundary")]


def test_preserves_token_spacing_and_punctuation_within_turn() -> None:
    turns = [SpeakerTurn(0, 2, "speaker_0")]
    tokens = [
        TimedTextToken(0.2, 0.4, " Hello"),
        TimedTextToken(0.4, 0.6, ","),
        TimedTextToken(0.6, 0.8, " world"),
        TimedTextToken(0.8, 1.0, "!  "),
    ]

    assert align_text_to_turns(turns, tokens) == [(turns[0], "Hello, world!")]


def test_coalesces_short_same_speaker_gaps_before_attribution() -> None:
    turns = [SpeakerTurn(0, 1, "speaker_0"), SpeakerTurn(2, 3, "speaker_0")]
    tokens = [
        TimedTextToken(0.2, 0.8, "First"),
        TimedTextToken(1.2, 1.8, " between"),
        TimedTextToken(2.2, 2.8, " second"),
    ]

    assert render_lines(turns, tokens, speaker_gap_seconds=2.0) == [
        "[0.000:3.000] speaker-0 -- First between second"
    ]


def test_coalesce_speaker_turns_respects_gap_boundaries_and_overlaps() -> None:
    assert coalesce_speaker_turns(
        [SpeakerTurn(0, 1, "speaker_0"), SpeakerTurn(5.999, 7, "speaker_0")],
        speaker_gap_seconds=5.0,
    ) == [SpeakerTurn(0, 7, "speaker_0")]
    assert coalesce_speaker_turns(
        [SpeakerTurn(0, 1, "speaker_0"), SpeakerTurn(6, 7, "speaker_0")],
        speaker_gap_seconds=5.0,
    ) == [SpeakerTurn(0, 1, "speaker_0"), SpeakerTurn(6, 7, "speaker_0")]
    assert coalesce_speaker_turns(
        [SpeakerTurn(0, 1, "speaker_0"), SpeakerTurn(7, 8, "speaker_0")],
        speaker_gap_seconds=5.0,
    ) == [SpeakerTurn(0, 1, "speaker_0"), SpeakerTurn(7, 8, "speaker_0")]
    assert coalesce_speaker_turns(
        [SpeakerTurn(0, 2, "speaker_0"), SpeakerTurn(1, 3, "speaker_0")],
        speaker_gap_seconds=0.0,
    ) == [SpeakerTurn(0, 3, "speaker_0")]
    assert coalesce_speaker_turns(
        [SpeakerTurn(0, 1, "speaker_0"), SpeakerTurn(1, 2, "speaker_0")],
        speaker_gap_seconds=0.0,
    ) == [SpeakerTurn(0, 1, "speaker_0"), SpeakerTurn(1, 2, "speaker_0")]
    equal_start_turns = [
        SpeakerTurn(0, 1, "speaker_0"),
        SpeakerTurn(0, 10, "speaker_1"),
        SpeakerTurn(0, 2, "speaker_0"),
    ]
    assert coalesce_speaker_turns(equal_start_turns, speaker_gap_seconds=5.0) == (
        equal_start_turns
    )


def test_intervening_speaker_prevents_coalescing_even_without_text() -> None:
    turns = [
        SpeakerTurn(0, 1, "speaker_0"),
        SpeakerTurn(1.1, 1.2, "speaker_1"),
        SpeakerTurn(1.3, 2, "speaker_0"),
    ]
    tokens = [
        TimedTextToken(0.2, 0.8, "First"),
        TimedTextToken(1.4, 1.8, "Second"),
    ]

    assert render_lines(turns, tokens, speaker_gap_seconds=5.0) == [
        "[0.000:1.000] speaker-0 -- First",
        "[1.300:2.000] speaker-0 -- Second",
    ]


def test_assigns_uncovered_tokens_to_nearest_turns() -> None:
    turns = [SpeakerTurn(2, 3, "speaker_0"), SpeakerTurn(5, 6, "speaker_1")]
    tokens = [
        TimedTextToken(1.0, 1.4, "before"),
        TimedTextToken(3.2, 3.4, " left"),
        TimedTextToken(3.5, 4.5, " tie"),
        TimedTextToken(4.6, 4.8, " right"),
        TimedTextToken(6.5, 6.8, " after"),
    ]

    assert align_text_to_turns(turns, tokens) == [
        (turns[0], "before left tie"),
        (turns[1], "right after"),
    ]


def test_omits_empty_zero_duration_and_turnless_tokens() -> None:
    turns = [SpeakerTurn(0, 1, "speaker_0")]
    tokens = [
        TimedTextToken(0.2, 0.7, "  "),
        TimedTextToken(0.2, 0.2, "instant"),
    ]

    assert align_text_to_turns(turns, tokens) == []
    assert align_text_to_turns([], [TimedTextToken(1, 2, "turnless")]) == []
    assert render_lines(turns, tokens) == []


def test_overlapping_turns_receive_separate_lines_by_best_overlap() -> None:
    turns = [SpeakerTurn(0, 2, "speaker_0"), SpeakerTurn(1, 3, "speaker_1")]
    tokens = [
        TimedTextToken(0.5, 1.8, "one"),
        TimedTextToken(2.1, 2.8, "two"),
    ]

    assert align_text_to_turns(turns, tokens) == [
        (turns[0], "one"),
        (turns[1], "two"),
    ]
    assert render_lines(turns, tokens) == [
        "[0.000:2.000] speaker-0 -- one",
        "[1.000:3.000] speaker-1 -- two",
    ]


def test_render_lines_formats_numeric_ids_and_repeated_ids_consistently() -> None:
    turns = [
        SpeakerTurn(0.125, 0.8, "0"),
        SpeakerTurn(1, 2, "0"),
        SpeakerTurn(2, 3, "1"),
        SpeakerTurn(3, 4, "2"),
    ]
    tokens = [
        TimedTextToken(0.2, 0.7, "First."),
        TimedTextToken(1.2, 1.8, "Again."),
        TimedTextToken(2.2, 2.8, "Second speaker."),
        TimedTextToken(3.2, 3.8, "Third speaker."),
    ]

    assert render_lines(turns, tokens, speaker_gap_seconds=0.0) == [
        "[0.125:0.800] speaker-0 -- First.",
        "[1.000:2.000] speaker-0 -- Again.",
        "[2.000:3.000] speaker-1 -- Second speaker.",
        "[3.000:4.000] speaker-2 -- Third speaker.",
    ]


def test_render_lines_normalizes_underscore_ids_and_preserves_other_labels() -> None:
    turns = [
        SpeakerTurn(0, 1, "speaker_0"),
        SpeakerTurn(1, 2, "speaker-1"),
        SpeakerTurn(2, 3, "guest"),
    ]
    tokens = [
        TimedTextToken(0.1, 0.9, "One."),
        TimedTextToken(1.1, 1.9, "Two."),
        TimedTextToken(2.1, 2.9, "Guest."),
    ]

    assert render_lines(turns, tokens) == [
        "[0.000:1.000] speaker-0 -- One.",
        "[1.000:2.000] speaker-1 -- Two.",
        "[2.000:3.000] guest -- Guest.",
    ]


def test_write_transcript_creates_utf8_file_with_newlines(tmp_path: Path) -> None:
    output = tmp_path / "transcript.txt"

    write_transcript(output, ["[0.000:1.000] speaker-0 -- café"])

    assert output.read_bytes() == "[0.000:1.000] speaker-0 -- café\n".encode()
    write_transcript(output, [])
    assert output.read_bytes() == b""

"""Timestamp alignment and text output helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class SpeakerTurn:
    start: float
    end: float
    speaker: str


@dataclass(frozen=True, slots=True)
class TextSegment:
    start: float
    end: float
    text: str


def align_text_to_turns(
    turns: list[SpeakerTurn], segments: list[TextSegment]
) -> list[tuple[SpeakerTurn, str]]:
    """Assign each timestamped text segment to its best-overlapping speaker turn."""
    assigned: dict[int, list[tuple[float, str]]] = {i: [] for i in range(len(turns))}

    for segment in segments:
        text = segment.text.strip()
        if not text or segment.end <= segment.start:
            continue

        overlaps = [
            (max(0.0, min(segment.end, turn.end) - max(segment.start, turn.start)), i)
            for i, turn in enumerate(turns)
        ]
        greatest = max((overlap for overlap, _ in overlaps), default=0.0)
        if greatest <= 0:
            continue

        candidates = [i for overlap, i in overlaps if overlap == greatest]
        midpoint = (segment.start + segment.end) / 2
        winner = next(
            (
                i
                for i in candidates
                if turns[i].start <= midpoint < turns[i].end
            ),
            candidates[0],
        )
        assigned[winner].append((segment.start, text))

    result: list[tuple[SpeakerTurn, str]] = []
    for i, turn in enumerate(turns):
        chunks = sorted(assigned[i], key=lambda item: item[0])
        if chunks:
            result.append((turn, " ".join(text for _, text in chunks)))
    return sorted(result, key=lambda item: (item[0].start, item[0].speaker))


def _format_speaker_label(speaker: str) -> str:
    """Return the display label for a numeric diarization speaker ID."""
    speaker_id = str(speaker)
    if speaker_id.isdecimal():
        return f"speaker-{speaker_id}"
    if speaker_id.startswith("speaker_") and speaker_id[8:].isdecimal():
        return f"speaker-{speaker_id[8:]}"
    if speaker_id.startswith("speaker-") and speaker_id[8:].isdecimal():
        return speaker_id
    return speaker_id


def render_lines(
    turns: list[SpeakerTurn], segments: list[TextSegment]
) -> list[str]:
    """Format assigned text as one line per speaker turn."""
    return [
        f"[{turn.start:.3f}:{turn.end:.3f}] {_format_speaker_label(turn.speaker)} -- {text}"
        for turn, text in align_text_to_turns(turns, segments)
    ]


def write_transcript(path: Path, lines: list[str]) -> None:
    """Write UTF-8 transcript lines, creating or truncating the output file."""
    path.write_text("".join(f"{line}\n" for line in lines), encoding="utf-8")

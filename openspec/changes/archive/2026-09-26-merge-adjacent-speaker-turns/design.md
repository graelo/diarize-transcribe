# Design

## Context

See [proposal.md](proposal.md) for motivation. The diarization adapter currently exposes raw model segments as `SpeakerTurn` values, and transcript rendering emits one line per such turn. The CLI forwards only the selected ASR language to the pipeline. The current token-attribution contract applies independently to every supplied turn.

## Goals / Non-Goals

**Goals:**

- Make continuous contributions by one speaker readable as one transcript line across brief silence gaps.
- Let users choose the silence threshold without changing the default five-second behavior.
- Preserve speaker changes, overlapping-speaker behavior, token attribution, and timestamp formatting.

**Non-Goals:**

- Change diarization-model settings or infer speaker identity beyond the model's labels.
- Merge turns separated by another diarized speaker, even when that intervening turn has no recognized text.
- Add paragraph formatting, punctuation restoration, or silence-based splitting between distinct speakers.

## Decisions

### Coalesce raw turns before token attribution

Prepare chronological raw diarization turns by grouping only adjacent turns with the same speaker when `next.start - current.end < speaker_gap_seconds`. A group uses the first turn's start and final turn's end, then existing token attribution runs against those coalesced turns.

This preserves a different-speaker boundary even if it would later be omitted for lack of text, and lets all attributed tokens in a merged contribution appear under one timestamp range. Coalescing after rendering would lack the raw sequence needed to preserve such boundaries; coalescing only visible lines could incorrectly join a speaker across an unrecognized intervening speaker turn.

### Expose one finite non-negative CLI duration

Add `--speaker-gap-seconds` as a float option with a default of `5.0`, validate finiteness and non-negativity before model loading, and pass it from the CLI through the pipeline to transcript preparation. A value of zero permits coalescing only where turns overlap; a gap equal to the threshold remains separate because the condition is strictly less than.

A configuration file or model-level parameter would make a simple per-invocation output preference less discoverable and is not needed for this CLI.

### Preserve raw boundaries across speakers and overlaps

Only immediately consecutive same-speaker raw turns are candidates. A different speaker resets the group. Turns with the same speaker that overlap have a negative temporal gap and therefore merge under every non-negative threshold; overlapping turns with different speakers remain separate.

## Risks / Trade-offs

- [A long within-speaker pause is visually significant] → The default limits merging to gaps below five seconds and users can reduce the threshold.
- [A short diarization error retains the same speaker label] → Coalescing cannot correct model labels; the threshold remains user-configurable.
- [Coalescing changes token-boundary attribution near silence gaps] → Apply the established overlap-first and nearest-turn fallback rules to the coalesced intervals, with focused regression tests.

## Migration Plan

The new option defaults to `5.0`, so existing invocations begin producing more readable coalesced output without command changes. Users who need raw segment boundaries can use `--speaker-gap-seconds 0`. No persisted data migration is required.

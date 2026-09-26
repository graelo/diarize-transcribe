---
number: 5
title: Attribute ASR segments to diarization turns by temporal overlap
date: 2026-09-24
status: superseded
links:
- target: 9
  kind: supersededby
---

# Attribute ASR segments to diarization turns by temporal overlap

## Context and Problem Statement

**Recorded retrospectively.** This decision was made and implemented on
2026-09-24. The diarization and ASR models run separately over the same
recording and emit timestamped speaker turns and text segments. The CLI must
produce a deterministic, one-line-per-speaker-turn transcript even when a text
segment crosses a speaker boundary or turns overlap.

Evidence: [initial OpenSpec design](../../openspec/changes/archive/2026-09-24-cli/design.md),
[alignment implementation](../../src/diarize_transcribe/transcript.py), and
[alignment tests](../../tests/test_transcript.py).

## Considered Options

- Assign each ASR segment to the diarization turn with the greatest temporal
  overlap.
- Implement speaker-masked or streaming ASR.
- Leave cross-boundary segments unassigned.

## Decision Outcome

Chosen option: **attribute each complete ASR text segment to the speaker turn
with the greatest temporal overlap**, because it works with the selected model
outputs while remaining deterministic and straightforward to test. Equal
overlaps prefer the turn containing the segment midpoint; turns are
start-inclusive and stop-exclusive. Text is ordered by segment start time, and
turns without assigned text are omitted.

### Consequences

- Good, because the attribution algorithm is deterministic and covered by unit
tests for boundary ties, gaps, and overlapping turns.
- Good, because the output contract is independent of the internal diarization
speaker-ID representation.
- Bad, because attribution is approximate at speaker changes and during
overlapping speech.
- Bad, because a more precise alignment strategy requires an explicit future
decision and corresponding output-contract review.

Superseded by ADR-0009: [Attribute timed ASR tokens to diarization turns by temporal overlap](0009-attribute-timed-asr-tokens-to-diarization-turns-by-temporal-overlap.md).

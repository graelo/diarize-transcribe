---
number: 10
title: Assign uncovered ASR tokens to the nearest diarization turn
date: 2026-09-26
status: accepted
links:
- target: 9
  kind: supersedes
---

# Assign uncovered ASR tokens to the nearest diarization turn

## Context and Problem Statement

ADR-0009 assigned timed ASR tokens only when they had positive temporal overlap
with a diarization turn. Local validation on a real recording showed small gaps
in diarization coverage around valid ASR tokens. Discarding those tokens clipped
word endings and fragments, making the transcript unusable.

Evidence: [continuity-fallback design](../../openspec/changes/attribute-asr-tokens-to-speaker-turns/design.md), [token alignment helper](../../src/diarize_transcribe/transcript.py), and [token-attribution decision](0009-attribute-timed-asr-tokens-to-diarization-turns-by-temporal-overlap.md).

## Considered Options

- Discard tokens with no positive diarization overlap.
- Assign tokens with no positive overlap to their nearest diarization turn.
- Revert to complete-sentence attribution.
- Add speaker-masked ASR or revise diarization boundaries.

## Decision Outcome

Chosen option: **assign a valid ASR token with no positive diarization overlap
to its nearest diarization turn**, because preserving recognized text is more
important than discarding it due to small temporal coverage gaps. Positive
overlap remains authoritative: greatest overlap wins and uses the token-midpoint
tie-break from ADR-0009. For the fallback, interval distance chooses the nearest
turn; equal distances select the earlier turn, then input order. Empty,
non-positive-duration tokens, and tokens with no available turns remain
unassigned.

### Consequences

- Good, because valid recognized token text is retained across small diarization
  coverage gaps and words are not clipped at turn boundaries.
- Good, because the fallback is deterministic and does not alter token text or
  the transcript line format.
- Bad, because a token in a coverage gap can be attributed to a nearby wrong
  speaker when diarization is inaccurate.
- Bad, because the fallback does not repair speaker-turn boundaries or solve
  overlapping-speech attribution.

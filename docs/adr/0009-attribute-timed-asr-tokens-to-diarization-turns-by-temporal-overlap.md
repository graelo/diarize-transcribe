---
number: 9
title: Attribute timed ASR tokens to diarization turns by temporal overlap
date: 2026-09-26
status: accepted
links:
- target: 5
  kind: supersedes
---

# Attribute timed ASR tokens to diarization turns by temporal overlap

## Context and Problem Statement

The selected Nemotron 3.5 ASR model returns aligned tokens with individual
start and end times, but the transcript pipeline previously reduced them to
whole sentences before attribution. Assigning a sentence that crosses a speaker
boundary to only one turn can misattribute substantial recognized text.

Evidence: [token-attribution OpenSpec proposal](../../openspec/changes/attribute-asr-tokens-to-speaker-turns/proposal.md), [Nemotron adapter](../../src/diarize_transcribe/models.py), [alignment helper](../../src/diarize_transcribe/transcript.py), and [superseded segment-level decision](0005-attribute-asr-segments-to-diarization-turns-by-temporal-overlap.md).

## Considered Options

- Assign each complete ASR sentence to the diarization turn with the greatest
  temporal overlap.
- Assign each timed ASR token to the diarization turn with the greatest temporal
  overlap.
- Use speaker-masked ASR to generate separate speaker transcripts.
- Leave text that crosses a speaker boundary unassigned.

## Decision Outcome

Chosen option: **assign each timed ASR token to the diarization turn with the
greatest temporal overlap**, because the selected ASR model already provides
aligned token timestamps and this allocates text more precisely at speaker
boundaries without changing the diarization model or transcript file format.
Ties use the turn containing the token midpoint, turns are start-inclusive and
stop-exclusive, and tokens with no positive overlap remain unassigned. Token
text is ordered by timestamp and concatenated without injected separators.

### Consequences

- Good, because text from a recognized sentence can be assigned to the distinct
  turns it actually overlaps rather than being attributed entirely to one
  speaker.
- Good, because preserving model-provided token spacing reconstructs recognized
  text without assumptions about words or punctuation.
- Good, because the deterministic overlap and tie-break rules remain testable
  and preserve the established transcript line format.
- Bad, because timestamp uncertainty near diarization boundaries can still place
  a token under the wrong speaker.
- Bad, because the transcript pipeline depends on aligned token output from the
  required ASR checkpoint; an ASR model without tokens would need another
  explicit decision.

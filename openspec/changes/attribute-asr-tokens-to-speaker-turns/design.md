# Design

## Context

See `proposal.md` for motivation and `specs/cli/spec.md` for the behavior contract. The Nemotron ASR adapter currently converts each aligned sentence to one `TextSegment`, discarding the sentence's timestamped tokens. The transcript helper then assigns the whole segment to one diarization turn and joins assigned segment strings with inserted spaces. Nemotron's aligned tokens expose text, start, and end values; their text already encodes the spacing needed to reconstruct the sentence.

ADR-0005 records complete-segment attribution. This change replaces that granularity while preserving the deterministic temporal-overlap rule, one-line-per-turn output, and diarization model.

## Goals / Non-Goals

**Goals:**
- Retain token-level timestamps and model-provided token text from Nemotron ASR output.
- Attribute each timed token to exactly one best-overlapping diarization turn.
- Reconstruct each turn's text without altering internal token spacing.
- Preserve deterministic tie breaking, transcript line format, and omission of turns without text.

**Non-Goals:**
- Change the diarization model or its speaker-turn boundaries.
- Add speaker-masked ASR, live streaming, or confidence-based attribution.
- Split one token across speakers, repair words, or modify the model's recognized text.
- Change CLI options or the transcript file format.

## Decisions

### Preserve a timed text-unit type across the ASR and alignment boundary

Replace sentence-only ASR normalization with a representation that carries each token's start time, end time, and text. The transcript alignment helper consumes these timed units rather than sentence aggregates.

This keeps the model adapter responsible for translating upstream model objects and keeps speaker attribution independent of the specific ASR library types.

Alternative: expose upstream `AlignedToken` objects to the transcript helper. Rejected because it couples application logic and tests to `mlx-audio` internals.

### Attribute one complete token to one turn

For every valid timed token, calculate overlap with every diarization turn and select the greatest-overlap turn. On equal overlap, use the token midpoint and the existing start-inclusive, stop-exclusive rule; retain the first candidate only when the midpoint resolves no tie. Tokens with no positive overlap remain unassigned.

Alternative: divide a cross-boundary token between turns. Rejected because subword tokens cannot be safely partitioned without changing recognized text.

### Concatenate token text exactly, then trim only output boundaries

Sort assigned tokens by start time and concatenate their `text` values directly. Trim leading and trailing whitespace only for the final rendered turn text; do not insert separators or normalize internal whitespace.

Alternative: join tokens with spaces, as the sentence implementation does. Rejected because Nemotron token strings include their own spacing and punctuation; adding separators corrupts reconstructed text.

### Supersede ADR-0005

Create an accepted ADR that supersedes ADR-0005. The new record documents token-level temporal attribution and its remaining limitations; ADR-0005 remains unmodified history.

## Risks / Trade-offs

- [Token timestamps are approximate near diarization boundaries] → Retain deterministic overlap and midpoint behavior, and cover boundary cases with unit tests.
- [Token text contains model-specific whitespace conventions] → Concatenate token text without injected separators and test leading-space and punctuation cases.
- [A model result has no tokens for a sentence] → Treat it as producing no assignable text rather than reconstructing from sentence text and losing attribution precision.
- [Token-level attribution increases output sensitivity to diarization boundaries] → Preserve the existing line format and expose only the improved allocation of text between turns.

## Migration Plan

Update the adapter, alignment helpers, and tests together. Existing callers retain the same CLI and transcript-file contract, but text crossing a speaker boundary can move to a different line. Roll back by reverting the token-attribution implementation and its superseding ADR if production reconciliation regresses.

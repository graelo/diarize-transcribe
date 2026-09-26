# Proposal

## Why

Nemotron ASR produces timestamped tokens, but the current pipeline assigns each complete sentence to a single diarization turn. Sentences spanning speaker boundaries can therefore place substantial text under the wrong speaker. Token-level attribution uses the alignment data already returned by the selected ASR model to improve speaker reconciliation. Real recordings also show that diarization coverage can contain small gaps around valid ASR tokens, so dropping no-overlap tokens can truncate recognized text.

## What Changes

- Preserve timestamped ASR tokens in the model adapter instead of reducing output to sentence-level text segments.
- Attribute each timed token independently to its best-overlapping diarization turn, retaining the current deterministic tie behavior.
- Assign a valid token that overlaps no diarization turn to its nearest turn so it is not discarded at a coverage gap.
- Concatenate the tokens assigned to a turn in timestamp order without changing their model-provided spacing; retain the current transcript line format and omission of turns without text.
- Record the continuity-fallback decision in a new ADR that supersedes ADR-0009.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `cli`: change speaker-attribution behavior from complete ASR segments to timed ASR tokens while preserving the transcript output format.

## Impact

- Affected code: ASR adapter, timestamp-alignment types and helpers, transcript rendering, and unit/model integration tests.
- User-visible behavior: text crossing a diarization boundary can be split between the corresponding speaker turns without truncating valid tokens at diarization coverage gaps.
- Dependencies and CLI options remain unchanged.
- Architecture record: ADR-0009 will be superseded without modifying its historical rationale.

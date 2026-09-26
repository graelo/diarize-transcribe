# Tasks

## 1. Preserve timed ASR tokens

- [x] 1.1 Replace sentence-only ASR normalization with a project-owned timed-token type carrying text, start, and end; verify adapter tests cover every returned token's timestamp and text.
- [x] 1.2 Flatten Nemotron sentence tokens in global timestamp order without exposing upstream `mlx-audio` token types outside the adapter; verify model-adapter tests preserve tokens from multiple sentences.

## 2. Attribute and render token text

- [x] 2.1 Update speaker attribution to select one best-overlapping turn for each valid timed token, retaining the existing midpoint tie-break and gap behavior; verify unit tests cover a sentence split across speaker turns, equal overlaps, gaps, and overlapping turns.
- [x] 2.2 Concatenate assigned token text in timestamp order without inserting or removing internal whitespace, trimming only the final turn boundaries; verify unit tests cover leading-space and punctuation tokens.
- [x] 2.3 Preserve transcript line formatting, speaker-label normalization, and omission of turns without assigned text; verify existing transcript rendering tests pass with timed tokens.

## 3. Document and verify the behavior

- [x] 3.1 Update README and the Unreleased changelog to describe token-level speaker attribution and its boundary limitations; verify no documentation describes complete-sentence attribution.
- [x] 3.2 Update the opt-in model smoke test to exercise timed-token attribution and verify timestamped, speaker-attributed transcript output for the two-speaker fixture.
- [x] 3.3 Run the default suite, the opt-in model smoke test, strict OpenSpec validation, and ADR health checks; verify all pass.

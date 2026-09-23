# Design

## Context

See `proposal.md` for motivation and `specs/cli/spec.md` for the behavior contract. Transcript formatting is centralized in `src/diarized_transcripts/transcript.py`: `render_lines` currently writes `SpeakerTurn.speaker` verbatim. The tested recording produced bare numeric speaker IDs, while existing unit-test fixtures also include underscore-prefixed IDs such as `speaker_0`.

## Goals / Non-Goals

**Goals:**
- Render numeric speaker IDs in output using the `speaker-<id>` form.
- Keep the diarization ID used internally for alignment unchanged.
- Keep the change limited to transcript presentation, tests, and the README example.

**Non-Goals:**
- Changing model inference, speaker assignment, turn alignment, timestamps, or transcript text.
- Rewriting existing transcript files or changing the underlying speaker IDs.

## Decisions

1. **Normalize IDs only at the rendering boundary.** Add a small formatter used by `render_lines`; do not change `SpeakerTurn.speaker` or model-adapter output. This keeps the internal diarization value available for deterministic ordering and attribution.

2. **Use a hyphenated `speaker-<id>` display label.** A bare numeric ID such as `0` renders as `speaker-0`. Normalize the model-style `speaker_0` form to the same display label, and leave an already canonical `speaker-0` unchanged. Preserve unrecognized nonnumeric identifiers as received rather than guessing at their meaning.

3. **Update tests and documentation with representative labels.** Unit tests should cover bare IDs `0`, `1`, and `2`, plus normalization of the existing underscore-prefixed form. The README transcript example should use `speaker-0` and `speaker-1`.

## Risks / Trade-offs

- **Model output may use a different speaker-ID representation in a future revision** → Keep normalization isolated in the renderer and test the observed bare numeric and underscore-prefixed forms; preserve unrecognized identifiers rather than silently rewriting them.
- **Consumers may parse the old bare-number label** → The output format change is intentional; existing transcript files are not modified.

## Migration Plan

No data migration is needed. Only newly generated transcript files use the new speaker labels.

# Proposal

## Why

Diarization emits multiple activity segments for one speaker around brief pauses, and the CLI currently renders each segment as a separate transcript line. This makes a continuous contribution difficult to read even when the diarizer has not identified a speaker change.

## What Changes

- Add a `--speaker-gap-seconds` CLI option, defaulting to `5.0`, to control when consecutive same-speaker diarization segments are combined.
- Coalesce consecutive segments for the same speaker only when their silence gap is strictly below the configured threshold, retaining the first start timestamp and final end timestamp.
- Keep segments separate when another speaker intervenes or their gap is at least the configured threshold.
- Reject negative speaker-gap thresholds before model inference.
- Update transcript documentation and tests for coalesced speaker-turn output.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `cli`: Add the configurable speaker-gap option and render coalesced same-speaker diarization turns rather than every raw activity segment.

## Impact

- Affected code: CLI option parsing, transcription pipeline parameters, and transcript turn preparation/rendering.
- Affected tests: CLI option forwarding and validation, pipeline forwarding, and speaker-turn attribution/rendering.
- Affected documentation: README output behavior and CLI option usage.

# Proposal

## Why

Bare numeric speaker IDs such as `0` are not very descriptive in a transcript. Prefixing them makes it clearer that the value identifies a speaker.

## What Changes

- Render numeric speaker IDs in transcript lines with a `speaker-` prefix, for example, `0` as `speaker-0`.
- Preserve the existing diarization, attribution, timestamps, and transcript text behavior.
- Update the README example and tests to use the new label format.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `cli`: Specify the speaker-ID label format in transcript output.

## Impact

Only the speaker-ID label in newly generated transcript files changes. Existing transcript files are unaffected; consumers that expect bare numeric IDs may need to adjust.

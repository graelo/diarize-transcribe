# Proposal

## Why

The project distribution is now named `diarize-transcribe`, while its installed executable is still `diarize`. Renaming the command to match the project makes the documented invocation consistent and clearly signals that the tool both diarizes and transcribes.

## What Changes

- **BREAKING:** Replace the `diarize` console command with `diarize-transcribe`; do not retain `diarize` as an alias.
- Update active README examples, tests, packaging metadata, and CLI usage references to use `diarize-transcribe`.
- Preserve all CLI options, validation, transcription behavior, and model requirements.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `cli`: Specify `diarize-transcribe` as the installed executable and remove the former `diarize` command.

## Impact

Affects `pyproject.toml`, `README.md`, CLI tests, and the `cli` capability spec. No dependency, model, or inference behavior changes are intended.

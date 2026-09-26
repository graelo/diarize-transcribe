# Proposal

## Why

The current Parakeet ASR adapter does not expose reliable explicit language control, while the project needs an ASR model with optional language prompting and timestamped output that continues to fit the diarization pipeline. Nemotron 3.5 ASR provides language-ID prompt conditioning, automatic detection by default, and aligned sentence timestamps through the existing `mlx-audio` integration.

## What Changes

- Replace the Parakeet checkpoint with `mlx-community/nemotron-3.5-asr-streaming-0.6b-8bit`; retain the existing Nemotron diarization model and no-fallback behavior.
- Add a generic `--language` option for supported model prompt keys. Default to `auto`; reject unsupported values instead of silently selecting a different prompt.
- **BREAKING**: remove `--chunk-seconds` and the application-managed fixed chunk/overlap behavior; use Nemotron's native streaming transcription path.
- Preserve timestamp-based speaker attribution and transcript formatting.
- Record the model-pair decision in a new accepted ADR that supersedes ADR-0003.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `cli`: switch ASR model, expose optional language prompting with automatic detection by default, and remove Parakeet-specific chunk controls.

## Impact

- Affected code: CLI, model adapters, pipeline, README, and CLI/model/pipeline tests.
- Affected architecture record: ADR-0003 will be superseded; its historical record remains unchanged.
- Dependency remains `mlx-audio==0.5.6`; no new runtime dependency is proposed.
- The ASR checkpoint is an MLX-native 8-bit Nemotron 3.5 model; the existing diarization model and transcript output format remain unchanged.

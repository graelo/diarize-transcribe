# Tasks

## 1. Replace the ASR adapter

- [x] 1.1 Set the ASR model constant to `mlx-community/nemotron-3.5-asr-streaming-0.6b-8bit` and call its native streaming API; verify adapter tests assert the model ID and timestamped sentence normalization.
- [x] 1.2 Pass the selected language prompt to ASR and validate explicit values against the loaded checkpoint's prompt dictionary; verify supported values are forwarded and unsupported values fail clearly without fallback.
- [x] 1.3 Remove Parakeet-specific external chunking and overlap arguments; verify the adapter uses the model-native streaming defaults and returned sentence times remain global.

## 2. Update the CLI and pipeline

- [x] 2.1 Remove `--chunk-seconds` and its validation/constants, add `--language` defaulting to `auto`, and forward the value through the pipeline; verify CLI help and invocation tests cover the default, explicit prompt, and removed option.
- [x] 2.2 Preserve speaker attribution and transcript formatting with Nemotron sentence timestamps; verify pipeline tests cover language forwarding and speaker-attributed output.

## 3. Update documentation and verify integration

- [x] 3.1 Update README model IDs, language option/default, automatic streaming behavior, and invocation examples; verify documentation matches CLI help and no longer advertises `--chunk-seconds`.
- [x] 3.2 Update the opt-in model smoke test to exercise Nemotron ASR with automatic language detection; verify its transcript segments have valid timestamps and the complete diarization pipeline still assigns at least two speakers.
- [x] 3.3 Run the default test suite and OpenSpec validation; verify all tests pass and the change validates against its CLI delta spec.

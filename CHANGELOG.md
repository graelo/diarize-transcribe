# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `--language` option for selecting a supported ASR language prompt, defaulting to automatic language detection.

### Changed

- Replace Parakeet with `mlx-community/nemotron-3.5-asr-streaming-0.6b-8bit` for timestamped transcription.
- Use Nemotron ASR's native streaming path for long recordings.
- Attribute timestamped ASR tokens independently to speaker turns, retaining valid tokens in diarization coverage gaps via nearest-turn fallback.

### Removed

- `--chunk-seconds`, which controlled Parakeet-specific application-managed chunking.

## [0.2.0] - 2026-09-26

### Added

- Chunked Parakeet transcription: speech recognition runs in 300-second chunks with a fixed 2-second overlap, bounding inference memory on long recordings while keeping timestamps relative to the beginning of the recording.
- `--chunk-seconds` option to select another finite chunk duration greater than 2 seconds.
- Opt-in end-to-end model integration test on a bundled two-speaker fixture (`RUN_MODEL_SMOKE=1 uv run pytest -m integration`).
- `run-model-tests` pull-request label that runs the model integration test as a required, merge-blocking check, skipped successfully otherwise.

### Changed

- Use the published `mlx-audio==0.5.6` package instead of pinning an upstream Git revision.

### Fixed

- Mitigated oversized Metal allocation failures during speech recognition on long recordings by bounding each inference chunk instead of processing the whole file at once.

## [0.1.0] - 2026-09-24

### Added

- Initial release of `diarize-transcribe`, a local CLI that transcribes audio recordings and labels each turn with a speaker using MLX on Apple Silicon.
- Fixed model pair: `mlx-community/Nemotron-3-Diarization` for diarization and `animaslabs/parakeet-tdt-0.6b-v3-mlx-8bit` for speech recognition, downloaded from Hugging Face on first run and never silently substituted.
- Speaker-turn transcripts in UTF-8 text, one line per turn in `[start:end] speaker-N -- text` format, with each recognized segment attributed to the diarization turn with the greatest temporal overlap.
- Required audio-input and `--output` transcript options, plus `--help` and `--version`.

[Unreleased]: https://github.com/graelo/diarize-transcribe/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/graelo/diarize-transcribe/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/graelo/diarize-transcribe/releases/tag/v0.1.0

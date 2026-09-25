# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Chunked Parakeet transcription: speech recognition runs in 300-second chunks with a fixed 2-second overlap, bounding inference memory on long recordings while keeping timestamps relative to the beginning of the recording.
- `--chunk-seconds` option to select another finite chunk duration greater than 2 seconds.

### Fixed

- Mitigated oversized Metal allocation failures during speech recognition on long recordings by bounding each inference chunk instead of processing the whole file at once.

## [0.1.0] - 2026-09-24

### Added

- Initial release of `diarize-transcribe`, a local CLI that transcribes audio recordings and labels each turn with a speaker using MLX on Apple Silicon.
- Fixed model pair: `mlx-community/Nemotron-3-Diarization` for diarization and `animaslabs/parakeet-tdt-0.6b-v3-mlx-8bit` for speech recognition, downloaded from Hugging Face on first run and never silently substituted.
- Speaker-turn transcripts in UTF-8 text, one line per turn in `[start:end] speaker-N -- text` format, with each recognized segment attributed to the diarization turn with the greatest temporal overlap.
- Required audio-input and `--output` transcript options, plus `--help` and `--version`.

[Unreleased]: https://github.com/graelo/diarize-transcribe/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/graelo/diarize-transcribe/releases/tag/v0.1.0

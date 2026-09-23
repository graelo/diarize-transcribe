# Proposal

## Why

Users need a simple local command-line workflow to turn an audio recording into speaker-attributed text without wiring separate models together themselves. This project will validate a small Python 3.14/uv package using MLX models on Apple Silicon, while keeping the transcript format predictable and easy to consume.

## What Changes

- Create an installable Python package with a Typer CLI, help/version options, validated audio input, and an output text-file parameter.
- Run Nemotron 3 Diarization and the specified Parakeet TDT ASR model, then associate recognized text with speaker turns.
- Write one formatted transcript line per speaker turn: `[starttime:stoptime] <speaker-id> -- <transcript>`.
- Document Apple Silicon/macOS expectations, model downloads, and the MLX Audio source revision needed for Nemotron support.

## Capabilities

### New Capabilities

- `cli`: Run local audio diarization and ASR from a CLI and save speaker-turn transcripts in the specified text format.

### Modified Capabilities

None.

## Impact

- New Python package, CLI, tests, and user documentation.
- Runtime dependencies include Typer and MLX Audio plus its MLX/audio stack; the tested MLX Audio source revision is required because PyPI `mlx-audio==0.5.5` lacks the Nemotron diarization loader.
- Downloads the Nemotron diarization and Parakeet ASR model weights from Hugging Face at first use. Runtime inference targets macOS on Apple Silicon.

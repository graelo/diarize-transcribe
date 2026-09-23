# Diarized Transcripts

A local CLI that transcribes audio and labels each transcript turn with a speaker, using MLX on Apple Silicon.

## Requirements

- macOS on Apple Silicon
- Python 3.14
- [uv](https://docs.astral.sh/uv/)
- Network access on first run to download the model weights from Hugging Face

`mlx-audio` is pinned to upstream commit `9ada37c1e33cfc99a7bdde0a902c0d4a0b913183`. The published `mlx-audio==0.5.5` does not include the Nemotron diarization loader, so do not replace the pinned Git dependency with that PyPI release.

## Install and run

```sh
uv sync --extra dev
uv run diarize recording.wav --output transcript.txt
```

To run the tagged v0.1 release directly from GitHub with `uvx`, without syncing the project environment:

```sh
uvx --from 'git+https://github.com/graelo/diarized-transcripts.git@v0.1' diarize recording.wav --output transcript.txt
```

Use `uv run diarize --help` for options or `uv run diarize --version` to print the package version. The CLI loads `mlx-community/Nemotron-3-Diarization` and `animaslabs/parakeet-tdt-0.6b-v3-mlx-8bit` on the first transcription run. It does not silently substitute another model.

Output is UTF-8 text, one line per speaker turn with assigned recognized text, for example:

```text
[0.000:1.420] speaker-0 -- Hello there.
[1.420:2.610] speaker-1 -- Hi.
```

Times are seconds from the beginning of the recording, rounded to milliseconds. Each timestamped Parakeet text segment is assigned to the diarization turn with the greatest temporal overlap; equal overlaps prefer the turn containing the segment midpoint. Segment-to-speaker attribution can be approximate at speaker changes and during overlapping speech.

## Development

```sh
uv sync --extra dev
uv run pytest
```

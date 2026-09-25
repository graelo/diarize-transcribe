# Diarize Transcribe

A local CLI that transcribes audio and labels each transcript turn with a speaker, using MLX on Apple Silicon.

## Requirements

- macOS on Apple Silicon
- Python 3.14
- [uv](https://docs.astral.sh/uv/)
- Network access on first run to download the model weights from Hugging Face

`mlx-audio==0.5.6` is installed from PyPI. This release includes the Nemotron diarization loader required by the project.

## Install and run

```sh
uv sync --extra dev
uv run diarize-transcribe recording.wav --output transcript.txt
```

Parakeet ASR uses 300-second chunks with a fixed 2-second overlap by default. Use `--chunk-seconds` to choose another finite chunk duration greater than 2 seconds:

```sh
uv run diarize-transcribe recording.wav --output transcript.txt --chunk-seconds 180
```

To run the tagged v0.2.0 release directly from GitHub with `uvx`, without syncing the project environment:

```sh
uvx --from 'git+https://github.com/graelo/diarize-transcribe.git@v0.2.0' diarize-transcribe recording.wav --output transcript.txt
```

Use `uv run diarize-transcribe --help` for options or `uv run diarize-transcribe --version` to print the package version. The CLI loads `mlx-community/Nemotron-3-Diarization` and `animaslabs/parakeet-tdt-0.6b-v3-mlx-8bit` on the first transcription run. It does not silently substitute another model.

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

The default test suite does not download model weights. To also run the opt-in
end-to-end integration test, which transcribes the bundled two-speaker fixture
through the real model pipeline and downloads the model weights on first run:

```sh
RUN_MODEL_SMOKE=1 uv run pytest -m integration
```

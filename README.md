# Diarize Transcribe

A local CLI that transcribes audio and labels each transcript turn with a speaker, using MLX on Apple Silicon.

## Requirements

- macOS on Apple Silicon
- Python 3.14
- [uv](https://docs.astral.sh/uv/)
- Network access on first run to download the model weights from Hugging Face

`mlx-audio==0.5.6` is installed from PyPI. This release includes the Nemotron diarization and Nemotron 3.5 ASR loaders required by the project.

## Install and run

```sh
uv sync --extra dev
uv run diarize-transcribe recording.wav --output transcript.txt
```

Nemotron 3.5 ASR uses its native streaming path for long recordings and automatic language detection by default. To select a supported language prompt explicitly, pass its model prompt key:

```sh
uv run diarize-transcribe recording.wav --output transcript.txt --language <prompt-key>
```

To run the tagged v0.2.0 release directly from GitHub with `uvx`, without syncing the project environment:

```sh
uvx --from 'git+https://github.com/graelo/diarize-transcribe.git@v0.2.0' diarize-transcribe recording.wav --output transcript.txt
```

Use `uv run diarize-transcribe --help` for options or `uv run diarize-transcribe --version` to print the package version. The CLI loads `mlx-community/Nemotron-3-Diarization` and `mlx-community/nemotron-3.5-asr-streaming-0.6b-8bit` on the first transcription run. It does not silently substitute another model.

Output is UTF-8 text, one line per speaker turn with assigned recognized text, for example:

```text
[0.000:1.420] speaker-0 -- Hello there.
[1.420:2.610] speaker-1 -- Hi.
```

Times are seconds from the beginning of the recording, rounded to milliseconds. Each timestamped Nemotron ASR token is assigned to the diarization turn with the greatest temporal overlap; equal overlaps prefer the turn containing the token midpoint. A token outside diarization coverage is assigned to its nearest turn so recognized text is retained. This allows text crossing a speaker boundary to be split between turns, but attribution can remain approximate at speaker changes and during overlapping speech.

## Development

```sh
uv sync --extra dev
uv run pytest
```

The default test suite does not download model weights. To also run the opt-in
end-to-end integration test, which transcribes the bundled two-speaker fixture
through the real Nemotron diarization and ASR pipeline and downloads the model
weights on first run:

```sh
RUN_MODEL_SMOKE=1 uv run pytest -m integration
```

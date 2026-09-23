# Tasks

## 1. Rename the installed command

- [x] 1.1 Change the project console-script entry and Typer application name to `diarize-transcribe`, updating CLI tests to check that help identifies the new command; verify project metadata exposes only `diarize-transcribe` and `--help` / `--version` work.

## 2. Update active documentation

- [x] 2.1 Replace README invocations and help/version references with `diarize-transcribe` for both `uv run` and `uvx`; verify no old command invocations remain in active documentation.

## 3. Validate the renamed CLI

- [x] 3.1 Run strict OpenSpec validation, `uv sync --extra dev --locked`, `uv build`, `env -u RUN_MODEL_SMOKE uv run pytest`, and `uv run diarize-transcribe --help` / `uv run diarize-transcribe --version`; verify build and CLI checks succeed, tests pass, and model smoke remains skipped.
- [x] 3.2 Verify no `diarize` console-script entry or active README invocation remains and that `.github/` and archived OpenSpec artifacts are unchanged.

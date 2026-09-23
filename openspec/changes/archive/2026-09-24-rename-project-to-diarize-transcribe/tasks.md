# Tasks

## 1. Rename package and module identifiers

- [x] 1.1 Move `src/diarized_transcripts` to `src/diarize_transcribe`, update source/test imports and the `pyproject.toml` package target while keeping the `diarize` script name; verify no `diarized_transcripts` imports remain in `src/` or `tests/`.
- [x] 1.2 Rename the project distribution to `diarize-transcribe`, regenerate `uv.lock` with uv, and run `uv sync --extra dev --locked`; verify the lockfile records the new local distribution name and the locked sync succeeds.

## 2. Update active documentation and validate

- [x] 2.1 Update the README title and GitHub `uvx` URL to `diarize-transcribe` while preserving the `diarize` command examples; verify the active README reflects both choices.
- [x] 2.2 Run strict OpenSpec validation, `uv build`, `env -u RUN_MODEL_SMOKE uv run pytest`, and `uv run diarize --help` / `uv run diarize --version`; verify the build and CLI checks succeed, tests pass, and the model smoke test remains skipped.
- [x] 2.3 Search active code, configuration, docs, and CI for old project/package identifiers and verify none remain; confirm no archived OpenSpec artifacts were changed.

# Tasks

## 1. Package and CLI Foundation

- [x] 1.1 Create the Python 3.14 `src/` package, uv project metadata, console entry point, and locked dependencies (including the tested pinned mlx-audio Git revision); verify `uv sync` succeeds on Apple Silicon macOS.
- [x] 1.2 Implement the Typer command with version/help and validated input/output file parameters; verify `uv run diarize --help`, `uv run diarize --version`, and a missing-input invocation behave as specified without loading models.

## 2. Model Inference and Alignment

- [x] 2.1 Add thin Nemotron and Parakeet model adapters using the specified Hugging Face IDs; verify adapter tests use the expected loader calls and an opt-in local smoke test loads both models.
- [x] 2.2 Implement timestamp-based assignment of recognized units to diarization turns, including greatest-overlap and midpoint tie-breaking; verify unit tests cover boundaries, ties, overlapping turns, ordering, and unassigned turns.
- [x] 2.3 Implement UTF-8 transcript rendering and output-file writing in the required format; verify formatting tests assert millisecond decimal timestamps, speaker IDs, text order, and empty-output behavior.

## 3. End-to-End Validation and Documentation

- [x] 3.1 Wire the CLI to validate platform/input, run both model stages, align results, and write the requested output; verify CLI tests cover success with mocked models and actionable model/platform failures.
- [x] 3.2 Document installation, Apple Silicon/macOS requirements, first-run model downloads, model IDs, and the mlx-audio source pin; verify the documented commands match the uv project configuration.
- [x] 3.3 Run the full automated test suite and CLI checks; verify `uv run pytest` and the help/version smoke checks pass with a clean project directory.

# Proposal

## Why

The project is being renamed to `diarize-transcribe`, but its package metadata, Python module, and README still use the old identity. Aligning the active project files avoids inconsistent installation and import names while retaining the established `diarize` command.

## What Changes

- **BREAKING:** Rename the Python distribution to `diarize-transcribe` and its import package to `diarize_transcribe`; update internal imports, tests, and packaging configuration accordingly.
- Update the lockfile and active README references, including the project heading and GitHub `uvx` URL to use the new repository slug.
- Preserve the existing `diarize` console command and all CLI behavior.
- Leave archived OpenSpec artifacts unchanged. The CI workflow currently contains no old project identifier and needs no name-specific edit.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. This is an identity and packaging rename; the existing CLI behavior and requirements do not change. The change opts out of spec deltas with `skip_specs: true`.

## Impact

Affects `pyproject.toml`, `uv.lock`, the Python package directory and imports under `src/`, tests, and `README.md`. The README's GitHub URL will assume the hosted repository uses the new `diarize-transcribe` slug; no Git remote is configured in this checkout to rename or verify the remote repository itself. No production dependencies or CI behavior are intended to change.

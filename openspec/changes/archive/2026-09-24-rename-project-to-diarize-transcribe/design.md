# Design

## Context

See `proposal.md` for the rename motivation and scope. `pyproject.toml` currently defines the `diarized-transcripts` distribution, maps the `diarize` executable to `diarized_transcripts.cli`, and tells Hatchling to package `src/diarized_transcripts`. The lockfile records the local distribution name. The source and tests import `diarized_transcripts`; the CI workflow itself does not contain either old identifier.

## Goals / Non-Goals

**Goals:**
- Make the distribution and Python import package consistently use `diarize-transcribe` and `diarize_transcribe` in active project files.
- Keep the `diarize` console command and runtime behavior unchanged.
- Update the active README title and installation URL while preserving historical archived artifacts.

**Non-Goals:**
- Rename the GitHub repository through a remote API; no Git remote is configured here.
- Add a compatibility import package for `diarized_transcripts`.
- Change CI triggers, runner, Python version, or test behavior.

## Decisions

1. **Rename the distribution and import package together.** Set the project name to `diarize-transcribe`, move the source package directory to `src/diarize_transcribe`, and update internal and test imports plus Hatchling's package path. This avoids shipping a new distribution that still exposes the old project-specific module namespace. Retaining an old import shim was considered but rejected because the request is to remove old active references and no compatibility requirement was given.

2. **Keep the console script name `diarize`.** Update only its target module path in `pyproject.toml`; keeping the command avoids an unnecessary CLI break and matches the user's explicit preference.

3. **Regenerate the project lock metadata with uv.** Update `uv.lock` through uv after changing `pyproject.toml` instead of hand-editing the local package record. Verify with a locked sync so CI and local installs use consistent metadata.

4. **Update active documentation, not history.** Change the README heading and its `uvx` GitHub URL to the new identity. Leave archived OpenSpec artifacts untouched. The current workflow has no old project name to replace, so verify it remains otherwise unchanged rather than editing CI gratuitously.

## Risks / Trade-offs

- **Python users importing `diarized_transcripts` will need to change imports** → Treat the rename as breaking as stated in the proposal; do not add a compatibility shim that leaves the old identity active.
- **The README install URL depends on the hosted repository adopting the new slug** → Update it to `graelo/diarize-transcribe`; note that the local checkout has no remote and cannot perform or verify the hosting rename.
- **The current branch contains archived notes with historical old paths** → Leave them unchanged by request and exclude archived material when checking for stale active references.

## Migration Plan

Rename files and imports, update metadata and README, regenerate `uv.lock`, then run a locked development sync, the full pytest suite, and CLI help/version checks. The GitHub-hosted repository slug must be renamed separately for the README URL to resolve. Rollback, if needed before release, is a revert of the rename commit; no compatibility migration is included.

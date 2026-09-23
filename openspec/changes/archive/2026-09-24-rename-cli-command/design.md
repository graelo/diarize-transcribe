# Design

## Context

See `proposal.md` for motivation and scope. `pyproject.toml` currently exposes the `diarize` console-script key, and `src/diarize_transcribe/cli.py` sets Typer's application name to `diarize`. README command examples and tests also use that name. CI runs the test suite and does not invoke the installed CLI.

## Goals / Non-Goals

**Goals:**
- Install only the `diarize-transcribe` console command and show that name in CLI help.
- Keep command options, validation, inference, and output behavior unchanged.
- Update all active user-facing invocations and relevant tests.

**Non-Goals:**
- Retain `diarize` as a compatibility alias.
- Change package imports, project metadata, model behavior, or CI configuration.

## Decisions

1. **Use `diarize-transcribe` as the executable.** It matches the distribution name and communicates both operations. `diarize` is shorter but would remain inconsistent with the project identity; `diarize-audio` is shorter than the selected name but less explicit about transcription.

2. **Update both the installed script key and Typer's application name.** Changing only `project.scripts` would install the new executable but could leave the help synopsis reporting `diarize`. Keep the help identity and executable name consistent.

3. **Do not provide an alias.** The requested operation is a rename, and the spec explicitly removes the former command. Update README examples and tests to make the new invocation the sole documented and tested name.

4. **Leave CI unchanged.** The workflow tests Python code but does not invoke the command; the normal unit suite and direct CLI checks cover the rename without adding environment or model requirements.

## Risks / Trade-offs

- **Existing users' `diarize` invocations stop working after updating →** Call out the breaking rename in the proposal and update all README examples to the replacement command.
- **An installed environment may retain a stale entry point until synchronized →** Verify the new command after `uv sync --extra dev --locked` and ensure the project metadata declares only the new script.

## Migration Plan

Users replace `diarize` with `diarize-transcribe`. After changing packaging metadata, synchronize the project environment and verify the new executable's help and version. Rollback is a revert of the change; no compatibility alias or dependency migration is included.

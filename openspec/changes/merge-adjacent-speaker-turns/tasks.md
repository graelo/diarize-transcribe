# Tasks

## 1. CLI configuration

- [ ] 1.1 Add the non-negative `--speaker-gap-seconds` float option with a `5.0` default and forward it through the CLI and pipeline; verify CLI tests cover help output, default forwarding, custom forwarding, and negative-value rejection before inference.

## 2. Speaker-turn coalescing

- [ ] 2.1 Implement chronological coalescing of adjacent same-speaker raw diarization turns before token attribution, preserving the first start and final end; verify transcript unit tests cover short gaps, gaps equal to the threshold, gaps above the threshold, zero-threshold behavior, and same-speaker overlaps.
- [ ] 2.2 Preserve distinct-speaker and token-attribution boundaries while rendering coalesced turns; verify transcript tests cover an intervening speaker turn, token allocation across a coalesced range, existing overlap handling, spacing, and no-text omission.

## 3. Documentation and validation

- [ ] 3.1 Update README and the Unreleased changelog for coalesced speaker output and `--speaker-gap-seconds`; verify no documentation still promises one line per raw diarization segment.
- [ ] 3.2 Update the opt-in model smoke test as needed for coalesced transcript output; verify `RUN_MODEL_SMOKE=1 uv run pytest -m integration` passes.
- [ ] 3.3 Sync the CLI delta into the canonical specification and run `uv run pytest`, strict OpenSpec validation, `adrs doctor`, and `git diff --check`; verify all checks pass.

# Tasks

## 1. Add attributed audio fixture and end-to-end coverage

- [x] 1.1 Move the supplied WAV to `tests/fixtures/two_speakers_15-20s.wav` and add fixture attribution documenting LibriSpeech CC BY 4.0, both utterance IDs and transcripts, and the inserted one-second silence; verify the fixture remains 17.175 seconds and the attribution file is present.
- [x] 1.2 Extend the `RUN_MODEL_SMOKE=1` integration test to run the real pipeline on the fixture and verify non-empty formatted output with at least two distinct speaker labels, without asserting exact transcript wording; verify routine `uv run pytest` skips the model test by default.
- [x] 1.3 Document the opt-in local integration-test command in the README Development section and verify it matches the test marker and environment guard.

## 2. Add reusable label-gated CI enforcement

- [x] 2.1 Add a separate GitHub Actions workflow for pull-request open, update, reopen, label, and unlabel events; use the `run-model-tests` label, read-only permissions, no secrets, a stable required-check name, and PR-scoped concurrency, and verify ordinary CI remains unchanged.
- [ ] 2.2 Configure the repository label and required branch-ruleset status check; verify that an unlabeled or unlabelled PR reports a successful skipped check, a labeled PR runs the model integration test and blocks merge on failure, and label removal clears the gate.
- [x] 2.3 Run `uv run pytest`, run the opt-in model integration test with model weights enabled on supported Apple Silicon macOS, and validate the OpenSpec change with `openspec validate opt-in-model-integration-tests --strict`.

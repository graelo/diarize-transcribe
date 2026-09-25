# Design

## Context

See `proposal.md` for motivation and `specs/ci/spec.md` for the required behavior. Routine CI currently runs `uv run pytest`; `tests/test_model_smoke.py` is opt-in through `RUN_MODEL_SMOKE=1` and only loads the fixed Nemotron and Parakeet models. ADR-0003 fixes that model pair and ADR-0006 establishes the tested `mlx-audio==0.5.6` integration.

The user-provided audio is a 17.175-second, mono 16 kHz PCM WAV. It combines LibriSpeech utterances `2277-149896-0000` (6.590 seconds) and `2035-147960-0010` (9.585 seconds), separated by one second of silence. The sources are released under CC BY 4.0; the fixture must retain attribution and note the concatenation. Its current size is about 537 KB.

## Goals / Non-Goals

**Goals:**
- Exercise real diarization and ASR inference together on a short, representative two-speaker sample when explicitly requested.
- Keep ordinary pull-request and `main` CI free of model downloads.
- Make the opt-in model result merge-blocking only while the request label is present, and successful/skipped when it is absent.
- Make the costly-test policy reusable for future model-backed integration tests.

**Non-Goals:**
- Run model downloads on every pull request or push to `main`.
- Assert exact ASR wording or promise transcription accuracy from one smoke sample.
- Change model selection, inference behavior, or the application CLI.
- Convert the existing WAV to lossy M4A; the small absolute size saving does not justify loss or another decoder variable.

## Decisions

### Keep the fixture as WAV and attribute its sources

Move the input file to `tests/fixtures/two_speakers_15-20s.wav` and add fixture documentation citing the LibriSpeech dataset, its CC BY 4.0 license, the two utterance IDs and transcripts, and the one-second silence added between them. Preserve the provided PCM WAV: it is already small and in a format suitable for the model stack. Do not attempt to identify the speakers beyond the dataset IDs.

### Turn the existing guarded model smoke test into an end-to-end check

Use the fixture with the existing `RUN_MODEL_SMOKE=1` opt-in guard and run the application pipeline so both required models perform inference. Assert that output is non-empty and structurally valid and includes at least two distinct speaker labels; avoid exact transcript strings and exact diarization boundaries, which can make the test brittle across model/runtime changes. Routine `uv run pytest` continues to skip this integration check.

### Put label-gated model testing in a separate workflow

Add a dedicated GitHub Actions workflow using ordinary `pull_request` events, not `pull_request_target`, with only read access and no secrets. Trigger on PR open, update, reopen, label, and unlabel events; run the model test only when `run-model-tests` is present. The workflow also triggers on pushes to `main` so the required check reports there: with no pull-request label to read, the job skips with a successful status and direct pushes to `main` are not blocked by the ruleset. A stable job/check name is required in the repository branch ruleset. GitHub reports a skipped job as successful, so the check passes without running when the label is absent; including the `unlabeled` event re-evaluates the check after the opt-in is withdrawn. Use PR-scoped concurrency (falling back to the ref for push events) so an updated or unlabeled PR can cancel a superseded model run.

The required check configuration and creation of the `run-model-tests` label are repository settings outside the workflow files. ADR-0007 records the proposed reusable policy; the CI workflow and behavior delta implement it.

## Risks / Trade-offs

- [Model output can vary and a short clip may not always yield two speaker IDs] → Assert structural output and distinct speakers rather than exact words or segment boundaries; establish the baseline on the supported runner before relying on it as a required check.
- [A skipped job may be misunderstood as a failed or missing check] → Keep one stable required check context, trigger on unlabeled events, and explicitly document that skipped means success when the label is absent.
- [A labeled PR downloads large model weights and consumes more runner time] → Run only on explicit opt-in, keep normal CI unchanged, and use no secrets or elevated permissions.
- [The audio contains redistributed third-party recordings] → Include source IDs, transcripts, dataset citation, CC BY 4.0 attribution, and the one-second edit description alongside the fixture.
- [Removing a label can withdraw the merge gate] → Make label changes auditable in the pull-request timeline and keep the branch-ruleset check name stable.

## Migration Plan

No application migration is required. Add the repository label and configure the model integration job as a required branch-ruleset check. Rollback consists of removing that required check and reverting the dedicated workflow/test change; routine CI remains independent.

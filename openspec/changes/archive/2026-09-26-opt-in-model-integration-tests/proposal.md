# Proposal

## Why

Routine CI deliberately avoids model downloads, while the existing opt-in smoke test only verifies that both models load. A short, attributed two-speaker fixture can support a real end-to-end integration check without slowing every pull request; when requested by label, that check should be required before merge.

## What Changes

- Add the LibriSpeech-derived WAV as a test fixture, with source IDs, transcripts, license attribution, and the one-second inter-utterance silence documented.
- Extend the opt-in model test to exercise the real diarization/transcription pipeline against the fixture and verify meaningful formatted output without depending on an exact transcript.
- Establish `run-model-tests` as the reusable pull-request label for heavyweight model integration tests. When present, the check runs and must pass before merge; when absent or removed, the job skips with a successful status and does not block merging. Ordinary CI remains model-download-free.
- Document label addition/removal and the required status-check behavior.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `ci`: distinguish routine model-download-free validation from label-triggered, merge-blocking model integration tests.

## Impact

- `.github/workflows/` for the opt-in pull-request workflow and required status check.
- `tests/test_model_smoke.py` and a fixture under `tests/fixtures/` for end-to-end model validation and source attribution.
- `openspec/specs/ci/spec.md` through a change-local spec delta.
- GitHub branch ruleset/status-check configuration to require the opt-in job; this configuration is outside the repository.
- Proposed ADR-0007 records the reusable cost-versus-validation policy. Existing model decisions in ADR-0003 and ADR-0006 remain unchanged.

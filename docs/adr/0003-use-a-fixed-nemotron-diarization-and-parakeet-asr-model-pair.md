---
number: 3
title: Use a fixed Nemotron diarization and Parakeet ASR model pair
date: 2026-09-24
status: superseded
links:
- target: 8
  kind: supersededby
---

# Use a fixed Nemotron diarization and Parakeet ASR model pair

## Context and Problem Statement

**Recorded retrospectively.** This decision was made and implemented on
2026-09-24. The initial CLI needed a tested local diarization model and a
separate timestamped speech-recognition model. A user-configurable model UI,
model fallback, and undocumented substitution were explicitly out of scope.

Evidence: [initial OpenSpec design](../../openspec/changes/archive/2026-09-24-cli/design.md),
[model adapters](../../src/diarize_transcribe/models.py), and
[model smoke test](../../tests/test_model_smoke.py).

## Considered Options

- Use `mlx-community/Nemotron-3-Diarization` and
  `animaslabs/parakeet-tdt-0.6b-v3-mlx-8bit` as a fixed pair.
- Offer model selection or a configurable model pair.
- Silently substitute a fallback model when one cannot load.

## Decision Outcome

Chosen option: **use the fixed Nemotron diarization and Parakeet ASR model
pair without fallback**, because both models were verified through the chosen
MLX Audio integration and fixed IDs make transcript behavior reproducible.
Model adapters isolate the upstream APIs from the rest of the application.

### Consequences

- Good, because users receive predictable model behavior and errors name the
  required model rather than masking a failed load with a substitution.
- Good, because model-specific API changes are contained in small adapters.
- Bad, because users cannot select another model and first use downloads both
  model weights.
- Bad, because adopting or replacing a model pair requires an explicit future
  decision.

Superseded by ADR-0008: [Use Nemotron 3.5 ASR for timestamped transcription with automatic language detection](0008-use-nemotron-3-5-asr-for-timestamped-transcription-with-automatic-language-detection.md).

---
number: 2
title: Run local inference on Apple-Silicon macOS through MLX
date: 2026-09-24
status: accepted
---

# Run local inference on Apple-Silicon macOS through MLX

## Context and Problem Statement

**Recorded retrospectively.** This decision was made and implemented on
2026-09-24. The initial command-line product needed to run speaker diarization
and transcription locally, using the MLX model ecosystem. The selected models
were verified on Python 3.14 running on Apple-Silicon macOS.

Evidence: [initial OpenSpec design](../../openspec/changes/archive/2026-09-24-cli/design.md),
[README requirements](../../README.md#requirements), and
[runtime platform guard](../../src/diarize_transcribe/cli.py).

## Considered Options

- Run the selected MLX models locally on Apple-Silicon macOS.
- Support CPU, CUDA, or other operating-system inference paths.
- Use a remote inference service.

## Decision Outcome

Chosen option: **run inference locally on Apple-Silicon macOS through MLX**,
because it provides the intended local workflow and is the platform on which
the required MLX models were tested. The CLI rejects unsupported platforms
with an actionable error; CPU, CUDA, and remote backends are not supported.

### Consequences

- Good, because inference remains local and the runtime path is small and
  reproducible.
- Good, because the supported-platform boundary is explicit in user-facing
  documentation and runtime validation.
- Bad, because the CLI is unavailable on non-macOS and non-Apple-Silicon
  systems; CI must use a compatible macOS runner.

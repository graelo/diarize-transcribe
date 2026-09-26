---
number: 8
title: Use Nemotron 3.5 ASR for timestamped transcription with automatic language detection
date: 2026-09-26
status: accepted
links:
- target: 3
  kind: supersedes
---

# Use Nemotron 3.5 ASR for timestamped transcription with automatic language detection

## Context and Problem Statement

The existing fixed model pair uses Nemotron for diarization and Parakeet for ASR. Parakeet does not provide the explicit language prompt control needed by the CLI, while the project requires timestamped recognition results that can continue through its speaker-attribution pipeline. Nemotron 3.5 ASR provides prompt-conditioned language control, automatic detection by default, native streaming, and aligned sentence timestamps.

Evidence: [OpenSpec change](../../openspec/changes/replace-parakeet-with-nemotron-asr/proposal.md), [Nemotron 3.5 ASR MLX checkpoint](https://huggingface.co/mlx-community/nemotron-3.5-asr-streaming-0.6b-8bit), and [prior fixed-pair decision](0003-use-a-fixed-nemotron-diarization-and-parakeet-asr-model-pair.md).

## Considered Options

- Keep the current fixed Nemotron diarization and Parakeet ASR pair.
- Replace Parakeet with the fixed Nemotron 3.5 ASR 8-bit MLX checkpoint and offer an optional language prompt.
- Allow users to select ASR models or silently fall back to another model.

## Decision Outcome

Chosen option: **replace Parakeet with `mlx-community/nemotron-3.5-asr-streaming-0.6b-8bit` while retaining `mlx-community/Nemotron-3-Diarization`**, with no model fallback. The CLI exposes an optional language prompt and defaults to `auto`, preserving automatic language detection unless a user explicitly chooses a supported prompt. Nemotron's native streaming path supplies aligned sentence timestamps to the existing speaker-attribution pipeline.

### Consequences

- Good, because the ASR model exposes explicit language control without selecting a forced language by default.
- Good, because timestamped sentence results preserve the existing diarization attribution and transcript format.
- Good, because a fixed model ID and no-fallback behavior keep model selection reproducible.
- Bad, because removing the Parakeet-specific `--chunk-seconds` option is a CLI breaking change.
- Bad, because the new ASR checkpoint must be downloaded on first use and changes the project's fixed ASR dependency.

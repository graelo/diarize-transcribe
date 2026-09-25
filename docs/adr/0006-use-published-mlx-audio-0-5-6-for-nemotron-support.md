---
number: 6
title: Use published mlx-audio 0.5.6 for Nemotron support
date: 2026-09-25
status: accepted
links:
- target: 4
  kind: supersedes
---

# Use published mlx-audio 0.5.6 for Nemotron support

## Context and Problem Statement

**Recorded retrospectively.** This decision was implemented on 2026-09-25 after `mlx-audio==0.5.6` was released with the Nemotron 3 diarization loader required by ADR-0003. The project no longer needs its direct Git dependency on upstream commit `9ada37c1e33cfc99a7bdde0a902c0d4a0b913183`. The 0.5.6 release successfully loaded both required models in the model smoke test.

Evidence: [project dependency](../../pyproject.toml), [locked package](../../uv.lock), [README runtime requirements](../../README.md), and [model smoke test](../../tests/test_model_smoke.py).

## Considered Options

- Use the published `mlx-audio==0.5.6` package from PyPI.
- Continue using the tested upstream Git revision.
- Track an unpinned upstream branch.

## Decision Outcome

Chosen option: **use the published `mlx-audio==0.5.6` package from PyPI**, because it includes the required Nemotron loader, passed the model smoke test for both required models, and avoids maintaining a direct source-repository dependency while keeping the dependency version explicit.

### Consequences

- Good, because installation uses an official published package and remains reproducible at a specific version.
- Good, because the required Nemotron and Parakeet model loaders are both covered by the successful smoke test.
- Bad, because a future compatible release still requires an explicit dependency and lockfile update.

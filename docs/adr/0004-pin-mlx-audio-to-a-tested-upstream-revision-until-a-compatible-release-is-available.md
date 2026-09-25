---
number: 4
title: Pin mlx-audio to a tested upstream revision until a compatible release is available
date: 2026-09-24
status: superseded
links:
- target: 6
  kind: supersededby
---

# Pin mlx-audio to a tested upstream revision until a compatible release is available

## Context and Problem Statement

**Recorded retrospectively.** This decision was made and implemented on
2026-09-24. The published `mlx-audio==0.5.5` release did not include the
Nemotron diarization loader required by ADR-0003. The tested upstream revision
`9ada37c1e33cfc99a7bdde0a902c0d4a0b913183` loaded both required model IDs and
completed a short Nemotron inference.

Evidence: [initial OpenSpec design](../../openspec/changes/archive/2026-09-24-cli/design.md),
[direct dependency pin](../../pyproject.toml), and
[model smoke test](../../tests/test_model_smoke.py).

## Considered Options

- Use the published `mlx-audio==0.5.5` release.
- Track an unpinned upstream branch.
- Pin the tested upstream commit as a direct Git dependency.

## Decision Outcome

Chosen option: **pin `mlx-audio` to the tested upstream revision
`9ada37c1e33cfc99a7bdde0a902c0d4a0b913183`**, because it provides the required
Nemotron loader while retaining a reproducible dependency revision. The PyPI
release is not a compatible substitute, and an unpinned branch would make the
runtime non-reproducible.

### Consequences

- Good, because a locked dependency revision preserves the verified model
  integration.
- Bad, because the project depends on an upstream Git commit rather than a
  published package release.
- Bad, because upstream compatibility must be actively revisited.

Supersede this ADR when an official `mlx-audio` release provides the required
Nemotron loader and the model smoke test passes against that release.

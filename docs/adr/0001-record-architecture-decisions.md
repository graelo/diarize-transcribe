---
number: 1
title: Record architecture decisions
date: 2026-09-24
status: accepted
---

# Record architecture decisions

## Context and Problem Statement

The project uses OpenSpec to record change-scoped requirements and design
rationale. Durable decisions that constrain multiple future changes need a
separate, decision-oriented record that is easy to find and can be
superseded without rewriting history.

## Decision Outcome

Chosen option: maintain concise Markdown Architecture Decision Records (ADRs)
in `docs/adr/`, managed with `adrs`. Use ADRs for cross-cutting, long-lived,
or difficult-to-reverse decisions; keep rationale local to a change in its
OpenSpec `design.md`.

## Consequences

- Good, because future changes can link to a stable record instead of
  duplicating durable rationale.
- Good, because a changed decision is documented by a new ADR that supersedes
  the earlier one.
- Bad, because the project must maintain a small, curated decision log instead
  of automatically converting every historical design decision into an ADR.

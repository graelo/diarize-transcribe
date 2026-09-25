---
number: 7
title: Use pull-request labels to gate expensive model integration tests
date: 2026-09-26
status: proposed
---

# Use pull-request labels to gate expensive model integration tests

## Context and Problem Statement

Routine CI must remain fast and avoid downloading large model weights, but model-backed integration tests provide confidence that the fixed local inference stack works end to end. Running those tests for every pull request is unnecessarily costly; leaving them manual and detached from merge checks makes failures easy to overlook.

Evidence: [CI specification](../../openspec/specs/ci/spec.md), [current model smoke test](../../tests/test_model_smoke.py), and [proposed OpenSpec design](../../openspec/changes/opt-in-model-integration-tests/design.md).

## Considered Options

- Run heavyweight model integration tests on every pull request.
- Require a maintainer to start a workflow manually, without a pull-request label.
- Use a reusable pull-request label to request the tests and make their check required while requested.

## Decision Outcome

**Proposed option:** use the reusable `run-model-tests` pull-request label to request heavyweight model integration tests. When the label is present, the test job runs and its required check must pass before merge. When it is absent or removed, the job is skipped with a successful status, so ordinary pull requests are not blocked and do not download model weights.

This balances explicit, merge-visible model validation with the cost and latency of downloading and running the models on every pull request. The implementation will use ordinary `pull_request` events, read-only repository permissions, and no secrets.

### Consequences

- Good, because maintainers can request end-to-end model validation and receive a merge-blocking result without imposing model downloads on routine CI.
- Good, because the same label policy can be reused by future heavyweight model integration tests.
- Bad, because model-backed validation is not run for unlabeled pull requests; reviewers must decide when the label is appropriate.
- Bad, because the required status check must also be configured in the repository's branch ruleset, outside the workflow files.

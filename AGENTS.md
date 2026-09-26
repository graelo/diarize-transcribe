# Agent Instructions

## Project References

Use the README as the source of truth for routine project work:

- [Requirements](README.md#requirements) defines the supported runtime and
  dependency constraints.
- [Install and run](README.md#install-and-run) defines the user-facing CLI
  workflow and model behavior.
- [Development](README.md#development) defines the development setup and test
  command. Consult it before running or changing checks.

Do not duplicate these commands here; update the README when the documented
workflow changes.

## Architecture Decision Records

This repository records durable architectural decisions in `docs/adr/` using
the `adrs` CLI.

Before finalizing a design or implementation, assess whether it creates,
changes, or reveals an ADR-worthy decision. Raise a concise ADR candidate when
the decision is cross-cutting, difficult to reverse, long-lived, affects a key
quality attribute, or constrains multiple future changes.

Do not create an ADR for change-local implementation details. Do not create,
edit, accept, or supersede an ADR unless the user requests or confirms it.

Before proposing a new ADR, search existing records to avoid duplication. One
ADR documents one decision. Link to supporting code, OpenSpec artifacts,
issues, or commits; distinguish confirmed facts from assumptions.

## OpenSpec Relationship

Use OpenSpec `design.md` for rationale local to a change. When a design relies
on or introduces a durable decision, link to the relevant ADR rather than
duplicating its rationale.

Do not alter archived OpenSpec artifacts to add ADR links. New ADRs may link
back to archived artifacts as historical evidence.

## Change Workflow

- Keep planning and implementation separate. Once OpenSpec planning artifacts
  are ready, recommend committing the planning changes and compacting the
  conversation, then stop. Wait for explicit user direction before creating the
  commit; after the commit, wait for separate explicit direction before starting
  implementation.

## ADR Lifecycle

Use `Proposed` for unsettled new decisions. For a historical implemented
decision, use `Accepted` and state that it was recorded retrospectively.

Accepted ADRs are append-only. When a decision changes, create a new ADR that
supersedes the earlier record; do not rewrite its rationale or history.

## ADR Commands

Run ADR commands from the repository root.

- Before proposing an ADR, search existing records:
  `adrs search <terms>`
- After the user approves a new decision record, create its skeleton without
  opening an interactive editor in the configured NextGen format:
  `adrs --ng new --no-edit --status Proposed "<title>"`
- For a confirmed historical decision, use `Accepted` and identify it as
  recorded retrospectively.
- To replace an accepted decision, create a new record with
  `adrs --ng new --no-edit --status Accepted --supersedes <number> "<title>"`.
  Do not rewrite the prior decision's rationale.
- After any ADR change, run:
  `adrs doctor`
  `adrs generate toc > docs/adr/README.md`

Do not re-run `adrs init` in an already initialized repository.

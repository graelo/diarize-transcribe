# Spec Delta

## Purpose

Automate validation of repository changes so pull requests and updates to the main branch receive consistent test results before release.

## ADDED Requirements

### Requirement: CI test workflow

The GitHub Actions workflow SHALL run the project's automated test suite for pull requests and for pushes to `main`, using Python 3.14 on a supported Apple Silicon macOS runner.

#### Scenario: Test a pull request

- **WHEN** a pull request is opened, updated, or reopened
- **THEN** the workflow runs the project's automated test suite in the supported environment and reports its result

#### Scenario: Test a push to main

- **WHEN** a commit is pushed to `main`
- **THEN** the workflow runs the project's automated test suite in the supported environment and reports its result

#### Scenario: Tests fail

- **WHEN** one or more tests fail
- **THEN** the workflow reports a failed check rather than a successful check

### Requirement: Keep model downloads out of routine CI

Routine CI runs SHALL NOT enable the opt-in model smoke test or download model weights.

#### Scenario: Run the routine test suite

- **WHEN** the workflow runs for a pull request or a push to `main`
- **THEN** it runs the automated test suite without enabling `RUN_MODEL_SMOKE` and without downloading model weights

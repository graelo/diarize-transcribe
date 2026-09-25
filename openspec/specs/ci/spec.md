# ci Specification

## Purpose
Automate validation of repository changes so pull requests and updates to the main branch receive consistent test results before release.

## Requirements

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

The routine CI test workflow SHALL run the project's automated test suite for pull requests and for pushes to `main`, using Python 3.14 on a supported Apple Silicon macOS runner. Routine CI runs SHALL NOT enable the opt-in model smoke test or download model weights. A separate label-triggered model integration check is governed by the requirement below and is not routine CI.

#### Scenario: Run the routine test suite

- **WHEN** routine CI runs for a pull request or a push to `main`
- **THEN** it runs the automated test suite without enabling `RUN_MODEL_SMOKE` and without downloading model weights

### Requirement: Gate heavyweight model integration tests by pull-request label

The project SHALL provide the reusable `run-model-tests` pull-request label to request model-backed integration tests on a representative two-speaker recording. While the label is present, the model integration check SHALL run for the pull request's current commit and SHALL be a required status check that blocks merging until it succeeds. When the label is absent or removed, the model job SHALL be skipped with a successful status check so it does not block merging or download model weights.

#### Scenario: Pull request does not have the model-test label

- **WHEN** a pull request is opened, updated, reopened, or has the `run-model-tests` label removed, and the label is absent
- **THEN** routine CI runs as usual, the model integration job is skipped with a successful status, and no model weights are downloaded

#### Scenario: Request model tests with the label

- **WHEN** the `run-model-tests` label is present on a pull request
- **THEN** the model integration check runs the end-to-end test on the supported Apple Silicon macOS environment and the required status remains unsuccessful if the test fails

#### Scenario: Update a labeled pull request

- **WHEN** a new commit is pushed to a pull request while the `run-model-tests` label is present
- **THEN** the model integration test runs against the updated commit and merge remains blocked until its required check succeeds

#### Scenario: Remove the label after requesting model tests

- **WHEN** the `run-model-tests` label is removed from a pull request
- **THEN** the model integration job is re-evaluated as skipped with a successful status, so the prior opt-in check no longer blocks merging

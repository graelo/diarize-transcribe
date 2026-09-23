# Proposal

## Why

Automated tests currently run locally but are not checked consistently before changes are merged or released. Running the test suite on pull requests and pushes to `main` will catch regressions earlier.

## What Changes

- Add a CI workflow that runs the project test suite for pull requests and pushes to `main`.
- Run CI in a supported Apple Silicon macOS environment using the project's Python and uv setup.
- Keep the model-download smoke test opt-in so routine CI does not download model weights.

## Capabilities

### New Capabilities

- `ci`: Automate test validation for pull requests and pushes to `main`.

### Modified Capabilities

None.

## Impact

Adds a GitHub Actions workflow and a new `ci` capability specification. No CLI behavior, production dependencies, or model behavior changes.

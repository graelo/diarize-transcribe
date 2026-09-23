# Tasks

## 1. Add the CI workflow

- [ ] 1.1 Create `.github/workflows/ci.yml` with `pull_request` and push-to-`main` triggers, `macos-latest`, and read-only `contents` permissions; verify the workflow declares the requested events and runner.
- [ ] 1.2 Set up Python 3.14 and uv, sync the locked development dependencies, then run `uv run pytest` without setting `RUN_MODEL_SMOKE`; verify the test suite passes and the model smoke test remains skipped.

## 2. Validate the change

- [ ] 2.1 Run `openspec validate ci-test-workflow --strict` and `uv run pytest`; confirm strict validation succeeds and all non-opt-in tests pass.

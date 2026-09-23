# Design

## Context

The repository has no existing GitHub Actions workflow. It targets Python 3.14 or newer and uses uv; the documented development test command is `uv run pytest`. The `mlx-audio` dependency and application runtime require Apple Silicon macOS. The model smoke test is marked as an integration test and skips unless `RUN_MODEL_SMOKE=1` is set.

## Goals / Non-Goals

**Goals:**
- Provide a consistent test check for pull requests and pushes to `main`.
- Use the selected GitHub-hosted `macos-latest` runner and Python 3.14.
- Avoid downloading model weights during routine CI.

**Non-Goals:**
- Configure repository branch protection or require the check for merging.
- Run model inference or the opt-in model smoke test in routine CI.
- Add release publishing, packaging, or deployment jobs.

## Decisions

1. **Use a single GitHub Actions workflow.** Add `.github/workflows/ci.yml` with `pull_request` and `push` triggers restricted to the `main` branch for pushes. A pull request trigger also runs when a pull request is opened, synchronized, or reopened. Keep workflow permissions read-only (`contents: read`); no secrets are needed.

2. **Use `macos-latest`.** This is the requested Apple Silicon runner label and currently resolves to an arm64 macOS runner. Pinning an OS-version-specific label or requiring a self-hosted runner would add maintenance or setup burden without a current need.

3. **Use the project’s existing uv test setup.** Install Python 3.14 and uv, sync the locked development dependencies, and run `uv run pytest`. This mirrors the documented local test path while detecting lockfile drift in CI.

4. **Leave model smoke testing opt-in.** Do not set `RUN_MODEL_SMOKE`; the ordinary test suite should continue to skip model downloads and inference.

## Risks / Trade-offs

- **The `macos-latest` image can move to a newer macOS/Xcode image** → Keep the runner label as requested; if an image update breaks compatibility, pin a supported macOS arm64 label and update this design/spec as needed.
- **A failing check does not by itself prevent merging** → Branch protection is explicitly out of scope; repository administrators can require the check separately.

## Migration Plan

No migration is required. Once merged, GitHub Actions will report checks for pull requests and pushes to `main`; the workflow does not change local development or model behavior.

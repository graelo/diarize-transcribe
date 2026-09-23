# Design

## Context

See `proposal.md` for motivation and `specs/cli/spec.md` for the behavior contract. The project is new, targets Python 3.14 on Apple Silicon macOS, and has no existing application code. A temporary Python 3.14 environment verified that both required model IDs load from `mlx-audio` source revision `9ada37c1e33cfc99a7bdde0a902c0d4a0b913183`; Nemotron also completed a short inference. The published PyPI `mlx-audio==0.5.5` does not include the Nemotron loader.

## Goals / Non-Goals

**Goals:**

- Keep the CLI thin and keep model inference, transcript alignment, and text rendering independently testable.
- Make the actual supported runtime and the source dependency pin reproducible with uv.
- Avoid model downloads for help/version and validate input before inference.

**Non-Goals:**

- Cross-platform CPU/CUDA support, speaker identity recognition, live microphone capture, or model fallback.
- A configurable model-selection UI, JSON/SRT/VTT output, or language-specific tuning in the first version.

## Decisions

1. **Use a small `src/` package with a Typer entry point.** Define a console script (command `diarize`) in `pyproject.toml`, accept the input as an `Annotated[Path, typer.Argument(...)]` with `exists=True`, `file_okay=True`, and `dir_okay=False`, and accept output as a writable path option. This keeps the CLI discoverable and gives tests a callable command entry point. A hand-written argparse CLI was considered but would duplicate the requested typed file validation and version/help behavior.

2. **Use the specified model IDs through mlx-audio and pin the tested upstream commit.** Load Nemotron with `mlx_audio.vad.load(..., strict=True)` and Parakeet with `mlx_audio.stt.load(...)`. Declare mlx-audio as a direct Git dependency pinned to `9ada37c1e33cfc99a7bdde0a902c0d4a0b913183`; an unpinned branch or PyPI 0.5.5 can fail to import the required Nemotron loader. Keep the model IDs fixed in the first version rather than allowing a fallback or undocumented substitution.

3. **Run diarization and ASR over the same recording, then align by timestamps.** Obtain diarization segments from Nemotron and timestamped recognized text segments (sentence intervals) from Parakeet. Assign each complete recognized text segment to the diarization turn with the greatest temporal overlap; for equal overlap, use the turn containing the segment midpoint, treating each turn as start-inclusive and stop-exclusive. Concatenate assigned text in temporal order per turn, and omit turns with no assigned text. This implements the user-selected one-line-per-speaker-turn format and yields deterministic handling of speaker-boundary words. It is simpler than implementing speaker-masked streaming ASR, while the exact required Parakeet model can be loaded through the selected mlx-audio revision.

4. **Render timestamps as decimal seconds with three fractional digits.** Use `[12.345:15.678] speaker_0 -- recognized words`, based on recording start. This matches the requested bracketed start/stop interval while making machine parsing and millisecond precision explicit.

5. **Keep runtime dependency validation explicit.** Set the package's minimum Python to 3.14. Document macOS/Apple Silicon as required for the MLX path and provide a clear runtime error on unsupported systems instead of attempting to load MLX modules and leaking a low-level import error.

## Risks / Trade-offs

- **Upstream source dependency is not a normal PyPI release** → Pin the tested commit in project metadata/lockfile and document why; revisit the pin once an official release contains the loader.
- **A Parakeet sentence can straddle a speaker change, or speakers can overlap** → Assign the complete timestamped sentence by greatest temporal overlap with midpoint tie-break and add unit tests for ties and overlapping turns; attribution remains approximate.
- **First run requires downloading large model weights and network access** → Document initial download behavior and surface actionable model-loading errors.
- **Model API/output schemas may change upstream** → Keep thin adapters, pin the tested revision, and add a smoke test for model result fields.

## Migration Plan

Not applicable; this is a new project with no existing users or data to migrate.

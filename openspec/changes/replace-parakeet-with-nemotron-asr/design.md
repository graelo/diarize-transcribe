# Design

## Context

See `proposal.md` for motivation and `specs/cli/spec.md` for the behavior contract. The current model adapter loads Parakeet and manually requests chunk duration plus overlap; the CLI exposes that tuning as `--chunk-seconds`. The installed Nemotron 3.5 ASR model accepts a `language` prompt (its checkpoint default is `auto`), uses native streaming with a 30-second default window, and returns sentence-level aligned timestamps. The existing transcript pipeline consumes timestamped `TextSegment` values and does speaker attribution independently of ASR model identity.

ADR-0003 fixes Parakeet as the ASR model in the model pair. This change replaces that decision without changing the diarization model or transcript format.

## Goals / Non-Goals

**Goals:**
- Use one explicit Nemotron 3.5 ASR checkpoint with no model fallback.
- Surface a generic, validated language-prompt option and retain automatic detection by default.
- Use the model's native streaming and timestamp output in place of Parakeet-specific external chunking.
- Preserve speaker-attribution semantics and output formatting.

**Non-Goals:**
- Add model selection or fallback behavior.
- Change the diarization model, transcript schema, or speaker-overlap attribution rule.
- Add live microphone streaming.
- Add a CLI control for native stream-window size in this change.

## Decisions

### Use the 8-bit MLX checkpoint

Use `mlx-community/nemotron-3.5-asr-streaming-0.6b-8bit`. It is directly loadable by the installed MLX Audio integration, matches the project's existing use of an 8-bit ASR checkpoint, and has a smaller download than the BF16 checkpoint. The model card reports quality matching BF16. Keep the model ID in one adapter constant so model failures identify the required checkpoint.

Alternative: use the full-precision BF16 checkpoint. It is also supported and can be reconsidered if integration testing finds material quality differences, but consumes more memory and download space.

### Make the language prompt optional and default to automatic detection

Expose `--language` as a string prompt key, defaulting to `auto`. After loading the model, validate a user-supplied key against the checkpoint's prompt dictionary and fail clearly if it is not supported; the upstream model otherwise falls back to its default prompt for unknown keys. Pass the validated value to `model.generate(..., language=...)`. Keep language identifiers and supported values data-driven rather than hard-coding a preferred locale in CLI code or documentation.

Alternative: accept any string and rely on the model's fallback. Rejected because a typo could silently produce transcription under a different prompt than requested.

### Use model-native streaming and aligned sentence output

Call the Nemotron model's native streaming `generate()` path without application-managed chunking or overlap parameters. Convert the returned aligned sentences to the existing `TextSegment` type; the pipeline and speaker-attribution code remain unchanged. Remove `--chunk-seconds` because its 300-second/2-second-overlap behavior is specific to the Parakeet adapter and does not map to Nemotron's native stream window.

Alternative: retain external overlapping chunks around Nemotron. Rejected because it duplicates the model's streaming behavior and would require reconciling timestamps and boundaries without a demonstrated benefit.

### Record the model change as an ADR superseding ADR-0003

Create a new accepted ADR for the fixed Nemotron diarization plus Nemotron 3.5 ASR pair, with automatic language detection as the default and explicit prompts as an optional user control. Leave ADR-0003 unchanged as historical context.

## Risks / Trade-offs

- [The model's native streaming output or timestamp boundaries differ from Parakeet's sentence output] → Normalize through the existing `TextSegment` adapter and verify whole-recording times in unit and opt-in model integration tests.
- [The checkpoint's language-prompt keys change] → Validate against the loaded checkpoint's prompt dictionary instead of maintaining a hard-coded locale list.
- [Users currently pass `--chunk-seconds`] → Document the breaking option removal and rely on the model's native streaming default.
- [Nemotron ASR behavior or checkpoint availability differs across `mlx-audio` environments] → Keep the package version pinned and make the existing opt-in end-to-end smoke test exercise the required model pair.

## Migration Plan

Update CLI callers to remove `--chunk-seconds`; Nemotron processes long files through its native streaming path. Users who need language conditioning may supply `--language <supported-prompt-key>`; omitting it keeps automatic detection. Roll back by reverting the model-switch commit if the new checkpoint fails compatibility or quality checks.

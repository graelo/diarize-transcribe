# Design

## Context

See `proposal.md` for the motivation and `specs/cli/spec.md` for the behavior contract. The current pipeline runs diarization and then transcription; only the Parakeet adapter calls ASR `model.generate`, with no chunking arguments. The pinned `mlx-audio` revision supports `chunk_duration` and `overlap_duration` and returns sentence objects with the fields consumed by the adapter. ADR-0003 and ADR-0004 constrain this work to the existing model pair and dependency revision.

## Goals / Non-Goals

**Goals:**
- Bound the duration of each non-streaming Parakeet inference chunk by default, while preserving the existing complete-file transcript workflow.
- Keep chunk settings explicit, validated, and testable without loading models in routine unit tests.
- Preserve the existing result adapter, speaker attribution, and transcript format.

**Non-Goals:**
- Chunk diarization, replace either model, change the pinned dependency, or add a streaming/live transcription mode.
- Promise that chunking prevents every possible OOM or that overlap reconciliation is lossless.
- Expose overlap as a separate CLI option in this change.

## Decisions

### Use the pinned Parakeet chunked-generation API

Pass the configured duration as `chunk_duration` and an explicit `overlap_duration=2.0` to Parakeet's existing non-streaming `model.generate` call. Keep the current `result.sentences` mapping to `TextSegment`; the pinned API adjusts chunk token timestamps and returns the same sentence-shaped result consumed by the adapter. This avoids custom waveform splitting, resampling, timestamp offsetting, and merging logic in the application.

Alternatives considered: external audio splitting or custom VAD-boundary splitting would require the application to own timestamp offsets and boundary reconciliation; streaming returns a different generator-oriented contract and is not a fit for this batch pipeline.

### Make 300 seconds the shared finite default

Use 300 seconds as the default chunk duration and allow users to override it with `--chunk-seconds`. Define the default once and reuse it across CLI, pipeline, and adapter so help text, direct API calls, and inference cannot drift. Validate the CLI input as finite and greater than 2 seconds before model loading. Keep overlap fixed at 2 seconds for a simple initial interface and because it matches the upstream default when chunking; the pinned API rejects overlap values equal to or greater than chunk duration.

At fixed encoder settings, attention-related memory is approximately quadratic in chunk duration; a five-minute window is roughly 1/144 the duration-squared allocation of a 60-minute window. This is a planning estimate, not a guarantee of peak process memory or a claim about the exact Metal allocation reported in the incident.

Alternatives considered: opt-in chunking would preserve the current failure for users who do not know to enable it; a shorter duration may add overhead without being necessary for the observed case, while a much longer duration raises peak memory. Allowing durations of 2 seconds or less would require dynamically reducing overlap, which conflicts with the fixed-overlap contract; these inputs are rejected instead. Custom defaults remain overridable.

### Preserve whole-recording timestamps and segment adaptation

Continue translating each returned sentence's start, end, and text into the existing `TextSegment` representation, then run the existing speaker attribution and transcript formatting unchanged. Rely on the pinned upstream implementation for chunk offsets and overlap reconciliation rather than applying a second offset in this application.

## Risks / Trade-offs

- [Upstream overlap merging is heuristic and can mis-handle divergent boundary transcripts] → Add adapter forwarding/result-shape tests and boundary-oriented tests where feasible; document that exact boundary text is not guaranteed. Do not implement a second merge layer.
- [The observed 115 GB request is not statically attributable to one exact tensor, and chunking cannot guarantee every file will fit] → Describe this as mitigation by bounded ASR chunk duration, preserve model errors, and leave the duration override available.
- [Nemotron still processes the full recording and retains duration-dependent data] → Keep the claim scoped to Parakeet ASR; diarization memory behavior is unchanged and is not solved here.
- [The application depends on upstream support in the pinned revision] → Test that chunk parameters are passed to a fake model and do not change the dependency pin; revisit only alongside a compatible pinned API change.

## Migration Plan

No data migration is required. Existing invocations gain default chunking; users can lower or raise chunk duration with `--chunk-seconds`. Transcript format and model IDs remain unchanged. Rollback consists of reverting this change; the CLI must not offer a no-chunking value that silently restores the original unbounded behavior.

# Tasks

## 1. Add configurable default chunking

- [ ] 1.1 Define the shared 300-second ASR chunk-duration default and 2-second overlap, and thread the chunk duration from the CLI through `run_transcription` to `transcribe_audio`; verify with pipeline and adapter unit tests that custom/default values reach `model.generate` as `chunk_duration` and `overlap_duration`.
- [ ] 1.2 Add `--chunk-seconds` with the shared default and finite-positive validation before inference; verify help displays the default and tests reject zero, negative, NaN, and infinity without calling the pipeline.
- [ ] 1.3 Preserve mapping of chunked result sentences to whole-recording `TextSegment` timestamps and existing speaker attribution/output; verify adapter tests cover sentence start, end, and text mapping without model downloads.

## 2. Document and validate the user-facing behavior

- [ ] 2.1 Document `--chunk-seconds`, its 300-second default, and the fixed 2-second overlap in the README usage section; verify the documented invocation matches `diarize-transcribe --help`.
- [ ] 2.2 Run the complete development test suite with `uv run pytest` and validate the OpenSpec change with `openspec validate chunk-long-audio-transcription --strict`; resolve any failures before implementation is considered complete.

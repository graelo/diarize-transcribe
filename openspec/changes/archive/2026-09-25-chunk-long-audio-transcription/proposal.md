# Proposal

## Why

Whole-file Parakeet inference can request an oversized Metal allocation on long recordings, failing before a transcript is produced. The pinned `mlx-audio` Parakeet API supports chunked inference, so the CLI can bound ASR inference memory without changing the required models or output format.

## What Changes

- Transcribe audio in bounded chunks by default, using a 300-second chunk duration and 2-second overlap.
- Add a `--chunk-seconds` option to let users choose a different finite chunk duration greater than 2 seconds, matching the fixed overlap constraint.
- Preserve whole-recording timestamps and the existing transcript output contract; document the setting and its default.
- Test CLI validation, forwarding of chunk settings through the pipeline and adapter, and timestamp-compatible chunk results without downloading model weights.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `cli`: the command gains configurable, default-on chunking for ASR while preserving the established transcript behavior.

## Impact

- CLI options and argument validation in `src/diarize_transcribe/cli.py`.
- Pipeline and Parakeet adapter call contract in `src/diarize_transcribe/pipeline.py` and `src/diarize_transcribe/models.py`.
- CLI and adapter tests, plus README usage documentation.
- No model IDs, pinned dependency, diarization behavior, or transcript format changes.

# Spec Delta

## MODIFIED Requirements

### Requirement: Command-line interface

The package SHALL provide a command-line application installed as the `diarize-transcribe` executable, with `--help` and `--version` options, required audio-input and transcript-output file parameters, and an optional `--language` option that accepts a prompt key supported by the ASR model and defaults to `auto`. The former `--chunk-seconds` option and `diarize` executable SHALL NOT be installed.

#### Scenario: Show help and version
- **WHEN** a user invokes `diarize-transcribe --help` or `diarize-transcribe --version`
- **THEN** the command displays usage identifying itself as `diarize-transcribe`, including `--language` and its `auto` default, or displays the installed package version, and exits successfully without loading models

#### Scenario: Accept an existing input file and output path
- **WHEN** a user invokes `diarize-transcribe` with an existing audio file as input and a transcript path as output
- **THEN** the command accepts the parameters and begins transcription using automatic language detection unless a supported `--language` prompt key is supplied

#### Scenario: Reject a missing input file
- **WHEN** a user invokes `diarize-transcribe` with an input path that does not exist or is not a file
- **THEN** the command reports a parameter error and does not begin model inference

#### Scenario: Reject an invalid chunk duration
- **WHEN** a user supplies the removed `--chunk-seconds` option
- **THEN** the command reports that the option is unsupported and does not begin model inference

#### Scenario: Reject an unsupported language prompt
- **WHEN** a user supplies a `--language` value that is not supported by the configured ASR checkpoint
- **THEN** the command reports an actionable parameter error and does not silently fall back to another language prompt

### Requirement: Local diarization and transcription

The application SHALL run Nemotron 3 Diarization from `mlx-community/Nemotron-3-Diarization` and speech recognition from `mlx-community/nemotron-3.5-asr-streaming-0.6b-8bit` on the supplied recording, and SHALL NOT silently substitute a different model. The application SHALL pass the selected language prompt to speech recognition, defaulting to `auto` when the user does not specify one.

#### Scenario: Process a recording
- **WHEN** the requested models are available and the input contains speech
- **THEN** the application obtains timestamped speaker activity and timestamped recognized text segments for producing speaker-attributed transcript turns

#### Scenario: Process a recording using automatic language detection
- **WHEN** the requested models are available and the input contains speech and no `--language` value is supplied
- **THEN** the application obtains timestamped speaker activity and timestamped recognized text using the ASR model's `auto` prompt for producing speaker-attributed transcript turns

#### Scenario: Process a recording with an explicit language prompt
- **WHEN** the requested models are available and the user supplies a supported `--language` prompt key
- **THEN** the application passes that exact key to speech recognition and obtains timestamped recognized text for producing speaker-attributed transcript turns

#### Scenario: Required model is unavailable or incompatible
- **WHEN** either required model cannot be downloaded, loaded, or run
- **THEN** the application reports which model failed and exits unsuccessfully without silently using another model

#### Scenario: Unsupported runtime platform
- **WHEN** the application is run outside a supported Apple Silicon macOS MLX environment
- **THEN** it reports that the local MLX runtime is unsupported and exits with a clear error

## REMOVED Requirements

### Requirement: Chunk long audio during speech recognition

**Reason**: This requirement specifies Parakeet-specific application-managed chunk duration and overlap; the selected ASR model already streams long recordings natively.

**Migration**: Remove `--chunk-seconds` and use Nemotron's built-in streaming path. Sentence timestamps remain relative to the original recording.

## ADDED Requirements

### Requirement: Native streaming transcription

The application SHALL process long recordings through the ASR model's native streaming transcription path without application-managed fixed-size chunks or overlap. Recognized sentence timestamps SHALL remain relative to the beginning of the original recording so existing speaker attribution and transcript formatting continue to apply.

#### Scenario: Transcribe a long recording
- **WHEN** a user supplies a recording longer than the model's native streaming window
- **THEN** the application processes it through native streaming without requiring a chunk-duration option or adding application-managed overlap

#### Scenario: Preserve whole-recording sentence timestamps
- **WHEN** speech recognition returns sentence timestamps while processing a recording through multiple native streaming windows
- **THEN** each sentence timestamp identifies its position from the beginning of the original recording and remains compatible with speaker attribution and transcript output

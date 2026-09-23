# Spec Delta

## Purpose

Provide a simple local command-line tool that diarizes an audio recording, transcribes its speech, and writes the recognized text with speaker-turn timestamps to a plain text file.

## ADDED Requirements

### Requirement: Command-line interface
The package SHALL provide a command-line application with `--help` and `--version` options and required audio-input and transcript-output file parameters.

#### Scenario: Show help and version
- **WHEN** a user invokes the command with `--help` or `--version`
- **THEN** the command displays usage information or the installed package version and exits successfully without loading models

#### Scenario: Accept an existing input file and output path
- **WHEN** a user invokes the command with an existing audio file as input and a writable transcript path as output
- **THEN** the command accepts the parameters and begins transcription

#### Scenario: Reject a missing input file
- **WHEN** a user invokes the command with an input path that does not exist or is not a file
- **THEN** the command reports a parameter error and does not begin model inference

### Requirement: Local diarization and transcription
The application SHALL run Nemotron 3 Diarization from `mlx-community/Nemotron-3-Diarization` and speech recognition from `animaslabs/parakeet-tdt-0.6b-v3-mlx-8bit` on the supplied recording, and SHALL NOT silently substitute a different model.

#### Scenario: Process a recording
- **WHEN** the requested models are available and the input contains speech
- **THEN** the application obtains timestamped speaker activity and timestamped recognized text segments for producing speaker-attributed transcript turns

#### Scenario: Required model is unavailable or incompatible
- **WHEN** either required model cannot be downloaded, loaded, or run
- **THEN** the application reports which model failed and exits unsuccessfully without silently using another model

#### Scenario: Unsupported runtime platform
- **WHEN** the application is run outside a supported Apple Silicon macOS MLX environment
- **THEN** it reports that the local MLX runtime is unsupported and exits with a clear error

### Requirement: Speaker-turn text output
The application SHALL write one UTF-8 text line per diarization speaker turn that has assigned recognized text, formatted as `[<start-seconds>:<stop-seconds>] <speaker-id> -- <transcript>`, with timestamps expressed as seconds from the start of the recording to millisecond precision. Speaker turns with no assigned recognized text SHALL be omitted.

#### Scenario: Write a speaker-turn transcript
- **WHEN** inference produces speaker turns and recognized text
- **THEN** the output file contains one formatted line for each turn with that turn's start and stop times, speaker ID, and assigned transcript text

#### Scenario: Attribute recognized text across speaker boundaries
- **WHEN** a recognized text segment overlaps more than one diarization speaker turn
- **THEN** the complete text segment is assigned to the turn with the greatest temporal overlap, with ties assigned to the turn containing the segment midpoint

#### Scenario: Handle overlapping speakers
- **WHEN** two speaker turns overlap in recording time
- **THEN** the output contains a separate line for each overlapping speaker turn that has assigned recognized text and preserves each line's turn timestamps and speaker ID

#### Scenario: No recognized speech
- **WHEN** inference produces no recognized text segments for any speaker turn
- **THEN** the application creates the requested output file with no transcript lines

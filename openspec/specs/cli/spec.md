# cli Specification

## Purpose

Provide a simple local command-line tool that diarizes an audio recording, transcribes its speech, and writes the recognized text with speaker-turn timestamps to a plain text file.

## Requirements

### Requirement: Command-line interface

The package SHALL provide a command-line application installed as the `diarize-transcribe` executable, with `--help` and `--version` options, required audio-input and transcript-output file parameters, an optional `--language` option that accepts a prompt key supported by the ASR model and defaults to `auto`, and an optional `--speaker-gap-seconds` option that accepts a finite non-negative duration and defaults to `5.0`. The former `--chunk-seconds` option and `diarize` executable SHALL NOT be installed.

#### Scenario: Show help and version
- **WHEN** a user invokes `diarize-transcribe --help` or `diarize-transcribe --version`
- **THEN** the command displays usage identifying itself as `diarize-transcribe`, including `--language` and its `auto` default and `--speaker-gap-seconds` and its `5.0` default, or displays the installed package version, and exits successfully without loading models

#### Scenario: Accept an existing input file and output path
- **WHEN** a user invokes `diarize-transcribe` with an existing audio file as input and a transcript path as output
- **THEN** the command accepts the parameters and begins transcription using automatic language detection and a 5.0-second speaker-gap threshold unless a supported `--language` prompt key or finite non-negative `--speaker-gap-seconds` value is supplied

#### Scenario: Configure the speaker-gap threshold
- **WHEN** a user supplies `--speaker-gap-seconds` with a non-negative duration
- **THEN** the command uses that exact duration to determine whether adjacent same-speaker diarization turns are coalesced

#### Scenario: Reject an invalid speaker-gap threshold
- **WHEN** a user supplies `--speaker-gap-seconds` with a non-finite or negative duration
- **THEN** the command reports a parameter error and does not begin model inference

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

### Requirement: Native streaming transcription

The application SHALL process long recordings through the ASR model's native streaming transcription path without application-managed fixed-size chunks or overlap. Recognized sentence timestamps SHALL remain relative to the beginning of the original recording so existing speaker attribution and transcript formatting continue to apply.

#### Scenario: Transcribe a long recording
- **WHEN** a user supplies a recording longer than the model's native streaming window
- **THEN** the application processes it through native streaming without requiring a chunk-duration option or adding application-managed overlap

#### Scenario: Preserve whole-recording sentence timestamps
- **WHEN** speech recognition returns sentence timestamps while processing a recording through multiple native streaming windows
- **THEN** each sentence timestamp identifies its position from the beginning of the original recording and remains compatible with speaker attribution and transcript output

### Requirement: Speaker-turn text output

The application SHALL coalesce consecutive diarization turns with the same speaker when the temporal gap from the current turn's end to the next turn's start is strictly less than the selected speaker-gap threshold; a different-speaker turn between two same-speaker turns SHALL prevent their coalescing. A coalesced turn SHALL use the first constituent turn's start time and the last constituent turn's end time. The application SHALL write one UTF-8 text line per coalesced diarization turn that has assigned recognized text, formatted as `[<start-seconds>:<stop-seconds>] <speaker-id> -- <transcript>`, with timestamps expressed as seconds from the start of the recording to millisecond precision. It SHALL assign each timed ASR token independently to the coalesced diarization turn with the greatest temporal overlap or, when no turn has positive overlap, to the nearest turn; it SHALL break equal nearest-turn distances toward the earlier turn. It SHALL concatenate tokens assigned to the same turn in timestamp order while preserving model-provided token spacing, and omit turns with no assigned recognized text.

#### Scenario: Write a speaker-turn transcript

- **WHEN** inference produces speaker turns and timed recognized tokens
- **THEN** the output file contains one formatted line for each coalesced turn with that turn's start and stop times, speaker ID, and assigned transcript text

#### Scenario: Coalesce a short same-speaker gap

- **WHEN** consecutive turns for the same speaker have a gap strictly below the selected speaker-gap threshold
- **THEN** the application renders one line using the first turn's start time, the last turn's end time, and text attributed across both turns

#### Scenario: Preserve a gap at the selected threshold

- **WHEN** consecutive turns for the same speaker have a gap equal to or greater than the selected speaker-gap threshold
- **THEN** the application renders separate lines for the turns when each has assigned recognized text

#### Scenario: Preserve an intervening speaker turn

- **WHEN** two turns for one speaker are separated by a turn for a different speaker
- **THEN** the application does not coalesce the same-speaker turns

#### Scenario: Attribute recognized text across speaker boundaries

- **WHEN** timed ASR tokens from one recognized sentence overlap more than one diarization speaker turn
- **THEN** each token is assigned independently to the turn with the greatest temporal overlap, with ties assigned to the turn containing that token's midpoint

#### Scenario: Assign a token in a diarization coverage gap

- **WHEN** a valid timed ASR token has no positive overlap with any diarization turn
- **THEN** the application assigns it to the temporally nearest turn, choosing the earlier turn when nearest distances are equal

#### Scenario: Preserve token text while assembling a turn

- **WHEN** multiple tokens assigned to one turn include model-provided leading spaces or punctuation
- **THEN** the turn transcript concatenates their text in timestamp order without inserting or removing internal whitespace

#### Scenario: Handle overlapping speakers

- **WHEN** two speaker turns overlap in recording time
- **THEN** the output contains a separate line for each overlapping speaker turn that has assigned recognized text and preserves each line's turn timestamps and speaker ID

#### Scenario: No recognized speech

- **WHEN** inference produces no recognized tokens for any speaker turn
- **THEN** the application creates the requested output file with no transcript lines

### Requirement: Speaker identifier labels

The application SHALL render each numeric diarization speaker ID `n` in transcript output as `speaker-n`.

#### Scenario: Render speaker ID zero

- **WHEN** a speaker turn has ID `0`
- **THEN** its transcript line uses `speaker-0`, not `0`

#### Scenario: Render other speaker IDs consistently

- **WHEN** speaker turns have IDs `1` and `2`
- **THEN** their transcript lines use `speaker-1` and `speaker-2`, respectively

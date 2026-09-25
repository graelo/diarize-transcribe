# Spec Delta

## MODIFIED Requirements

### Requirement: Command-line interface

The package SHALL provide a command-line application installed as the `diarize-transcribe` executable, with `--help` and `--version` options, required audio-input and transcript-output file parameters, and a `--chunk-seconds` option that defaults to 300 seconds and accepts only finite values greater than 2 seconds. The former `diarize` executable SHALL NOT be installed.

#### Scenario: Show help and version

- **WHEN** a user invokes `diarize-transcribe --help` or `diarize-transcribe --version`
- **THEN** the command displays usage information identifying itself as `diarize-transcribe`, including the chunk duration option and its default in help, or the installed package version, and exits successfully without loading models

#### Scenario: Accept an existing input file and output path

- **WHEN** a user invokes `diarize-transcribe` with an existing audio file as input and a writable transcript path as output
- **THEN** the command accepts the parameters and begins transcription using the default chunk duration unless another valid duration is supplied

#### Scenario: Reject a missing input file

- **WHEN** a user invokes `diarize-transcribe` with an input path that does not exist or is not a file
- **THEN** the command reports a parameter error and does not begin model inference

#### Scenario: Reject an invalid chunk duration

- **WHEN** a user supplies a value less than or equal to 2 seconds, or a non-finite value, for `--chunk-seconds`
- **THEN** the command reports a parameter error and does not begin model inference

## ADDED Requirements

### Requirement: Chunk long audio during speech recognition

The application SHALL run speech recognition using chunks with the duration selected by `--chunk-seconds` (300 seconds by default, and always greater than 2 seconds) and a 2-second overlap between chunks. Recognized text segment timestamps SHALL remain relative to the beginning of the original recording so existing speaker attribution and transcript formatting continue to apply.

#### Scenario: Transcribe a recording using default chunk settings

- **WHEN** a user runs the application without specifying `--chunk-seconds`
- **THEN** speech recognition uses a 300-second chunk duration and a 2-second overlap

#### Scenario: Transcribe a recording using a custom chunk duration

- **WHEN** a user supplies a finite value greater than 2 seconds for `--chunk-seconds`
- **THEN** speech recognition uses that duration with a 2-second overlap

#### Scenario: Preserve whole-recording segment timestamps

- **WHEN** speech recognition returns segments from more than one chunk
- **THEN** each segment timestamp identifies its position from the beginning of the original recording and remains compatible with speaker attribution and transcript output

# Spec Delta

## MODIFIED Requirements

### Requirement: Command-line interface

The package SHALL provide a command-line application installed as the `diarize-transcribe` executable, with `--help` and `--version` options and required audio-input and transcript-output file parameters. The former `diarize` executable SHALL NOT be installed.

#### Scenario: Show help and version

- **WHEN** a user invokes `diarize-transcribe --help` or `diarize-transcribe --version`
- **THEN** the command displays usage information identifying itself as `diarize-transcribe`, or the installed package version, and exits successfully without loading models

#### Scenario: Accept an existing input file and output path

- **WHEN** a user invokes `diarize-transcribe` with an existing audio file as input and a writable transcript path as output
- **THEN** the command accepts the parameters and begins transcription

#### Scenario: Reject a missing input file

- **WHEN** a user invokes `diarize-transcribe` with an input path that does not exist or is not a file
- **THEN** the command reports a parameter error and does not begin model inference

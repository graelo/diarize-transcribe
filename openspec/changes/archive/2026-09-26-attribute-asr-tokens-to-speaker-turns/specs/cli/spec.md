# Spec Delta

## MODIFIED Requirements

### Requirement: Speaker-turn text output

The application SHALL write one UTF-8 text line per diarization speaker turn that has assigned recognized text, formatted as `[<start-seconds>:<stop-seconds>] <speaker-id> -- <transcript>`, with timestamps expressed as seconds from the start of the recording to millisecond precision. It SHALL assign each timed ASR token independently to the diarization turn with the greatest temporal overlap or, when no turn has positive overlap, to the nearest turn; it SHALL break equal nearest-turn distances toward the earlier turn. It SHALL concatenate tokens assigned to the same turn in timestamp order while preserving model-provided token spacing, and omit turns with no assigned recognized text.

#### Scenario: Write a speaker-turn transcript

- **WHEN** inference produces speaker turns and timed recognized tokens
- **THEN** the output file contains one formatted line for each turn with that turn's start and stop times, speaker ID, and assigned transcript text

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

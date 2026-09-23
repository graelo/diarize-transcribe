## ADDED Requirements

### Requirement: Speaker identifier labels

The application SHALL render each numeric diarization speaker ID `n` in transcript output as `speaker-n`.

#### Scenario: Render speaker ID zero

- **WHEN** a speaker turn has ID `0`
- **THEN** its transcript line uses `speaker-0`, not `0`

#### Scenario: Render other speaker IDs consistently

- **WHEN** speaker turns have IDs `1` and `2`
- **THEN** their transcript lines use `speaker-1` and `speaker-2`, respectively

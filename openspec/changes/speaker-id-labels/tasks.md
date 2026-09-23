## 1. Speaker ID rendering

- [ ] 1.1 Add a speaker-label formatter at the transcript-rendering boundary so numeric IDs render as `speaker-<id>`, `speaker_<id>` is normalized to the same form, and internal turn IDs remain unchanged.
- [ ] 1.2 Update transcript unit tests to cover IDs `0`, `1`, and `2`, underscore-prefixed normalization, already canonical labels, repeated IDs across turns, and unchanged timestamps/text.
- [ ] 1.3 Update the README transcript example to use `speaker-0` and `speaker-1`.

## 2. Validation

- [ ] 2.1 Run the test suite and strict OpenSpec validation; confirm speaker attribution, timing, and transcript content behavior remain unchanged apart from the rendered speaker label.

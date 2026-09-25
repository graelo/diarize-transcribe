# Test fixtures

## two_speakers_15-20s.wav

A 17.175-second, mono, 16 kHz, 16-bit PCM recording of two speakers used by the
opt-in model integration test (`RUN_MODEL_SMOKE=1`).

It was assembled from two LibriSpeech utterances with one second of silence
inserted between them:

| # | Utterance ID     | Speaker ID | Duration | Transcript                                                                                             |
|---|------------------|------------|----------|--------------------------------------------------------------------------------------------------------|
| 1 | 2277-149896-0000 | 2277       | 6.590 s  | HE WAS IN A FEVERED STATE OF MIND OWING TO THE BLIGHT HIS WIFE'S ACTION THREATENED TO CAST UPON HIS ENTIRE FUTURE                        |
| 2 | 2035-147960-0010 | 2035       | 9.585 s  | I EXPLAINED TO ANTONIA HOW THIS MEANT THAT HE WAS TWENTY FOUR YEARS OLD THAT HE MUST HAVE BEEN THERE WHEN WHITE MEN FIRST CAME LEFT ON FROM BUFFALO AND INDIAN TIMES |

Layout: utterance 1 spans 0.000–6.590 s, inserted silence spans 6.590–7.590 s,
and utterance 2 spans 7.590–17.175 s.

Source: [LibriSpeech](https://www.openslr.org/12) (OpenSLR SR12, also published
as [`openslr/librispeech_asr` on Hugging Face](https://huggingface.co/datasets/openslr/librispeech_asr)),
distributed under the
[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)
license. The utterances are reused here under that license; this note provides
the required attribution.

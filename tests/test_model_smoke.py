import os

import pytest


@pytest.mark.integration
@pytest.mark.skipif(
    os.environ.get("RUN_MODEL_SMOKE") != "1",
    reason="set RUN_MODEL_SMOKE=1 to download and load model weights",
)
def test_loads_both_required_models() -> None:
    from mlx_audio.stt import load as load_asr
    from mlx_audio.vad import load as load_vad

    diarizer = load_vad("mlx-community/Nemotron-3-Diarization", strict=True)
    asr = load_asr("animaslabs/parakeet-tdt-0.6b-v3-mlx-8bit")

    assert diarizer is not None
    assert asr is not None

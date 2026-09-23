from pathlib import Path
from types import ModuleType, SimpleNamespace

from diarized_transcripts.models import (
    ASR_MODEL,
    DIARIZATION_MODEL,
    diarize_audio,
    transcribe_audio,
)


def test_model_adapters_use_required_ids_and_normalize_outputs(monkeypatch, tmp_path: Path) -> None:
    calls: list[tuple[str, str]] = []
    diar_module = ModuleType("mlx_audio.vad")
    asr_module = ModuleType("mlx_audio.stt")

    class FakeDiarizer:
        def generate(self, audio: str):
            calls.append(("diarize", audio))
            return SimpleNamespace(
                segments=[SimpleNamespace(start=0.1, end=1.4, speaker="speaker_0")]
            )

    class FakeAsr:
        def generate(self, audio: str):
            calls.append(("transcribe", audio))
            return SimpleNamespace(
                sentences=[SimpleNamespace(start=0.2, end=1.2, text="Hello.")]
            )

    diar_module.load = lambda model_id, strict: (  # type: ignore[attr-defined]
        calls.append(("load_diar", model_id)) or FakeDiarizer()
    )
    asr_module.load = lambda model_id: (  # type: ignore[attr-defined]
        calls.append(("load_asr", model_id)) or FakeAsr()
    )
    monkeypatch.setitem(__import__("sys").modules, "mlx_audio.vad", diar_module)
    monkeypatch.setitem(__import__("sys").modules, "mlx_audio.stt", asr_module)

    audio = tmp_path / "sample.wav"
    assert diarize_audio(audio)[0].speaker == "speaker_0"
    assert transcribe_audio(audio)[0].text == "Hello."
    assert ("load_diar", DIARIZATION_MODEL) in calls
    assert ("load_asr", ASR_MODEL) in calls
    assert calls.count(("diarize", str(audio))) == 1
    assert calls.count(("transcribe", str(audio))) == 1

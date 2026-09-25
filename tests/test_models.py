from pathlib import Path
from types import ModuleType, SimpleNamespace

from diarize_transcribe.models import (
    ASR_CHUNK_OVERLAP_SECONDS,
    ASR_MODEL,
    DEFAULT_ASR_CHUNK_SECONDS,
    DIARIZATION_MODEL,
    diarize_audio,
    transcribe_audio,
)
from diarize_transcribe.transcript import TextSegment


def test_model_adapters_use_required_ids_and_normalize_outputs(monkeypatch, tmp_path: Path) -> None:
    calls: list[tuple] = []
    diar_module = ModuleType("mlx_audio.vad")
    asr_module = ModuleType("mlx_audio.stt")

    class FakeDiarizer:
        def generate(self, audio: str):
            calls.append(("diarize", audio))
            return SimpleNamespace(
                segments=[SimpleNamespace(start=0.1, end=1.4, speaker="speaker_0")]
            )

    class FakeAsr:
        def generate(
            self, audio: str, *, chunk_duration: float, overlap_duration: float
        ):
            calls.append(("transcribe", audio, chunk_duration, overlap_duration))
            return SimpleNamespace(
                sentences=[SimpleNamespace(start=300.2, end=301.2, text="Hello.")]
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
    assert transcribe_audio(audio) == [TextSegment(300.2, 301.2, "Hello.")]
    assert transcribe_audio(audio, chunk_seconds=75.5) == [
        TextSegment(300.2, 301.2, "Hello.")
    ]
    assert ("load_diar", DIARIZATION_MODEL) in calls
    assert ("load_asr", ASR_MODEL) in calls
    assert calls.count(("diarize", str(audio))) == 1
    assert calls.count(
        (
            "transcribe",
            str(audio),
            DEFAULT_ASR_CHUNK_SECONDS,
            ASR_CHUNK_OVERLAP_SECONDS,
        )
    ) == 1
    assert calls.count(
        ("transcribe", str(audio), 75.5, ASR_CHUNK_OVERLAP_SECONDS)
    ) == 1

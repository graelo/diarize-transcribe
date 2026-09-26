from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest

from diarize_transcribe.models import (
    ASR_MODEL,
    DEFAULT_ASR_LANGUAGE,
    DIARIZATION_MODEL,
    ModelError,
    diarize_audio,
    transcribe_audio,
)
from diarize_transcribe.transcript import TimedTextToken


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
        prompt_dictionary = {"auto": 0, "test-language": 1}

        def generate(self, audio: str, *, language: str):
            calls.append(("transcribe", audio, language))
            return SimpleNamespace(
                sentences=[
                    SimpleNamespace(
                        tokens=[
                            SimpleNamespace(start=301.0, end=301.2, text=" later"),
                        ]
                    ),
                    SimpleNamespace(
                        tokens=[
                            SimpleNamespace(start=300.2, end=300.7, text="Hello"),
                            SimpleNamespace(start=300.7, end=300.9, text="."),
                        ]
                    ),
                ]
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
    expected_tokens = [
        TimedTextToken(300.2, 300.7, "Hello"),
        TimedTextToken(300.7, 300.9, "."),
        TimedTextToken(301.0, 301.2, " later"),
    ]
    assert diarize_audio(audio)[0].speaker == "speaker_0"
    assert transcribe_audio(audio) == expected_tokens
    assert transcribe_audio(audio, language="test-language") == expected_tokens
    assert ("load_diar", DIARIZATION_MODEL) in calls
    assert ("load_asr", ASR_MODEL) in calls
    assert calls.count(("diarize", str(audio))) == 1
    assert calls.count(("transcribe", str(audio), DEFAULT_ASR_LANGUAGE)) == 1
    assert calls.count(("transcribe", str(audio), "test-language")) == 1


def test_transcribe_audio_rejects_unsupported_language_prompt(monkeypatch, tmp_path: Path) -> None:
    asr_module = ModuleType("mlx_audio.stt")

    class FakeAsr:
        prompt_dictionary = {"auto": 0}

        def generate(self, *args, **kwargs):
            raise AssertionError("unsupported prompts must not reach generation")

    asr_module.load = lambda model_id: FakeAsr()  # type: ignore[attr-defined]
    monkeypatch.setitem(__import__("sys").modules, "mlx_audio.stt", asr_module)

    with pytest.raises(ModelError, match="unsupported language prompt 'test-language'"):
        transcribe_audio(tmp_path / "sample.wav", language="test-language")

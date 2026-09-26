from pathlib import Path
import tomllib

from click import unstyle
import pytest
from typer.testing import CliRunner

from diarize_transcribe import __version__
from diarize_transcribe import cli
from diarize_transcribe.models import DEFAULT_ASR_LANGUAGE
from diarize_transcribe.pipeline import ModelError

runner = CliRunner()


def test_help_and_version_exit_before_inference(monkeypatch) -> None:
    def unexpected(*args, **kwargs):
        raise AssertionError("models must not load")

    monkeypatch.setattr(cli, "run_transcription", unexpected)
    monkeypatch.setenv("COLUMNS", "200")

    help_result = runner.invoke(cli.app, ["--help"], prog_name="diarize-transcribe")
    version_result = runner.invoke(cli.app, ["--version"])

    help_output = unstyle(help_result.stdout)
    assert help_result.exit_code == 0
    assert "Usage: diarize-transcribe" in help_output
    assert "--output" in help_output
    assert "--language" in help_output
    assert DEFAULT_ASR_LANGUAGE in help_output
    assert "--speaker-gap-seconds" in help_output
    assert "5.0" in help_output
    assert "--chunk-seconds" not in help_output
    assert version_result.exit_code == 0
    assert version_result.stdout.strip() == __version__


def test_only_new_console_command_is_registered() -> None:
    project = tomllib.loads(
        (Path(__file__).parents[1] / "pyproject.toml").read_text(encoding="utf-8")
    )

    assert project["project"]["scripts"] == {
        "diarize-transcribe": "diarize_transcribe.cli:app"
    }


def test_cli_writes_requested_transcript(monkeypatch, tmp_path: Path) -> None:
    audio = tmp_path / "audio.wav"
    audio.write_bytes(b"audio")
    output = tmp_path / "transcript.txt"
    requests: list[tuple[str, float]] = []
    monkeypatch.setattr(cli, "_supported_platform", lambda: True)

    def fake_transcription(
        path: Path, *, language: str, speaker_gap_seconds: float
    ) -> list[str]:
        requests.append((language, speaker_gap_seconds))
        return ["[0.000:1.000] speaker_0 -- Hello."]

    monkeypatch.setattr(cli, "run_transcription", fake_transcription)

    result = runner.invoke(
        cli.app,
        [
            str(audio),
            "--output",
            str(output),
            "--language",
            "test-language",
            "--speaker-gap-seconds",
            "2.5",
        ],
    )

    assert result.exit_code == 0, result.output
    assert requests == [("test-language", 2.5)]
    assert output.read_text(encoding="utf-8") == "[0.000:1.000] speaker_0 -- Hello.\n"


def test_cli_uses_automatic_language_detection_by_default(
    monkeypatch, tmp_path: Path
) -> None:
    audio = tmp_path / "audio.wav"
    audio.touch()
    output = tmp_path / "transcript.txt"
    requests: list[tuple[str, float]] = []
    monkeypatch.setattr(cli, "_supported_platform", lambda: True)
    monkeypatch.setattr(
        cli,
        "run_transcription",
        lambda path, *, language, speaker_gap_seconds: requests.append(
            (language, speaker_gap_seconds)
        )
        or [],
    )

    result = runner.invoke(cli.app, [str(audio), "--output", str(output)])

    assert result.exit_code == 0, result.output
    assert requests == [(DEFAULT_ASR_LANGUAGE, 5.0)]


@pytest.mark.parametrize("speaker_gap_seconds", ["-0.1", "nan", "inf", "-inf"])
def test_cli_rejects_invalid_speaker_gap_before_inference(
    monkeypatch, tmp_path: Path, speaker_gap_seconds: str
) -> None:
    audio = tmp_path / "audio.wav"
    audio.touch()
    monkeypatch.setattr(cli, "_supported_platform", lambda: True)
    monkeypatch.setattr(
        cli,
        "run_transcription",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("must not run")),
    )

    result = runner.invoke(
        cli.app,
        [
            str(audio),
            "--output",
            str(tmp_path / "out.txt"),
            "--speaker-gap-seconds",
            speaker_gap_seconds,
        ],
    )

    assert result.exit_code != 0
    assert "--speaker-gap-seconds" in result.output
    assert "must not run" not in result.output


def test_cli_rejects_removed_chunk_option_before_inference(
    monkeypatch, tmp_path: Path
) -> None:
    audio = tmp_path / "audio.wav"
    audio.touch()
    monkeypatch.setattr(
        cli,
        "run_transcription",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("must not run")),
    )

    result = runner.invoke(
        cli.app,
        [str(audio), "--output", str(tmp_path / "out.txt"), "--chunk-seconds", "75.5"],
    )

    assert result.exit_code != 0
    assert "No such option: --chunk-seconds" in result.output
    assert "must not run" not in result.output


def test_cli_rejects_missing_input_before_model_loading(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(
        cli,
        "run_transcription",
        lambda path: (_ for _ in ()).throw(AssertionError("must not run")),
    )

    result = runner.invoke(
        cli.app, [str(tmp_path / "missing.wav"), "--output", str(tmp_path / "out.txt")]
    )

    assert result.exit_code != 0
    assert "does not exist" in result.output


def test_cli_reports_model_failure_without_traceback(monkeypatch, tmp_path: Path) -> None:
    audio = tmp_path / "audio.wav"
    audio.touch()
    monkeypatch.setattr(cli, "_supported_platform", lambda: True)
    monkeypatch.setattr(
        cli,
        "run_transcription",
        lambda path, **kwargs: (_ for _ in ()).throw(ModelError("Nemotron load failed")),
    )

    result = runner.invoke(cli.app, [str(audio), "--output", str(tmp_path / "out.txt")])

    assert result.exit_code == 1
    assert "Nemotron load failed" in result.output
    assert "Traceback" not in result.output


def test_cli_explains_unsupported_platform(monkeypatch, tmp_path: Path) -> None:
    audio = tmp_path / "audio.wav"
    audio.touch()
    monkeypatch.setattr(cli, "_supported_platform", lambda: False)
    monkeypatch.setattr(
        cli,
        "run_transcription",
        lambda path, **kwargs: (_ for _ in ()).throw(AssertionError()),
    )

    result = runner.invoke(cli.app, [str(audio), "--output", str(tmp_path / "out.txt")])

    assert result.exit_code == 1
    assert "macOS on Apple Silicon" in result.output

from pathlib import Path
import tomllib

from click import unstyle
from typer.testing import CliRunner

from diarize_transcribe import __version__
from diarize_transcribe import cli
from diarize_transcribe.pipeline import ModelError

runner = CliRunner()


def test_help_and_version_exit_before_inference(monkeypatch) -> None:
    def unexpected(*args, **kwargs):
        raise AssertionError("models must not load")

    monkeypatch.setattr(cli, "run_transcription", unexpected)

    help_result = runner.invoke(
        cli.app, ["--help"], prog_name="diarize-transcribe"
    )
    version_result = runner.invoke(cli.app, ["--version"])

    help_output = unstyle(help_result.stdout)
    assert help_result.exit_code == 0
    assert "Usage: diarize-transcribe" in help_output
    assert "--output" in help_output
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
    monkeypatch.setattr(
        cli, "run_transcription", lambda path: ["[0.000:1.000] speaker_0 -- Hello."]
    )

    result = runner.invoke(cli.app, [str(audio), "--output", str(output)])

    assert result.exit_code == 0, result.output
    assert output.read_text(encoding="utf-8") == "[0.000:1.000] speaker_0 -- Hello.\n"


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
    monkeypatch.setattr(
        cli,
        "run_transcription",
        lambda path: (_ for _ in ()).throw(ModelError("Nemotron load failed")),
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
        cli, "run_transcription", lambda path: (_ for _ in ()).throw(AssertionError())
    )

    result = runner.invoke(cli.app, [str(audio), "--output", str(tmp_path / "out.txt")])

    assert result.exit_code == 1
    assert "macOS on Apple Silicon" in result.output

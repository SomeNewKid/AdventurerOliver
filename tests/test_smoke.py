"""Smoke tests for Adventurer Oliver."""

import adventurer_oliver.cli as cli
from adventurer_oliver.cli import main


def test_cli_prints_agent_response(capsys, monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """Verify the CLI accepts an adventure request."""
    monkeypatch.setattr(
        cli,
        "get_agent_response",
        lambda prompt: f"Recommendation for {prompt}",
    )

    exit_code = main(["cozy quest"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == "Recommendation for cozy quest\n"

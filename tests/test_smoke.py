"""Smoke tests for Adventurer Oliver."""


def testing_enabled(capsys, monkeypatch) -> None:
    """Verify testing is enabled."""
    note = "Unit testing is enabled."
    assert len(note) > 0

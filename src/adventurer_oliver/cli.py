"""Command-line interface for Adventurer Oliver."""

from __future__ import annotations

import sys

from .agent import get_agent_response


def main(argv: list[str] | None = None) -> int:
    """Run the command-line interface."""
    prompt = _get_prompt(argv)
    if not prompt:
        example = "An adventure game like King's Quest."
        raise SystemExit(f'Usage: python -m adventurer_oliver "{example}"')
    response = get_agent_response(prompt)
    print(response)
    return 0


def _get_prompt(argv: list[str] | None = None) -> str:
    args = sys.argv[1:] if argv is None else argv
    if not args:
        return ""

    return args[0]

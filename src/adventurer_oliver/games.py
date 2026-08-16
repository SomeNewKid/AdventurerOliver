from __future__ import annotations

import random


def get_text_adventure_game() -> str:
    """Return a random text adventure game."""
    games = [
        "The Hitchhiker's Guide to the Galaxy",
        "Colossal Cave Adventure",
        "Trinity",
        "The Lurking Horror",
        "Adventureland",
    ]
    game = random.choice(games)
    print(f"get_text_adventure_game() returning: {game}")
    return game


def get_graphical_adventure_game() -> str:
    """Return a random graphical adventure game."""
    games = [
        "The Secret of Monkey Island",
        "Day of the Tentacle",
        "Grim Fandango",
        "The Longest Journey",
        "Space Quest",
    ]
    game = random.choice(games)
    print(f"get_graphical_adventure_game() returning: {game}")
    return game

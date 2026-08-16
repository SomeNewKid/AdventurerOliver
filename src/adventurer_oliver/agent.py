"""OpenAI Agents SDK integration for Adventurer Oliver."""

from __future__ import annotations

from agents import Agent, ModelSettings, Runner, function_tool

from .games import get_graphical_adventure_game, get_text_adventure_game

_MODEL_NAME = "gpt-5"

_INSTRUCTIONS = """
You recommend PC computer adventure games.

The user will ask for a recommendation, often by naming an adventure game they
already know or have already played.

You must call exactly one available recommendation tool before answering:

- Call recommend_text_adventure_game when the user is asking for something like
  a parser-based or text adventure game.
- Call recommend_graphical_adventure_game when the user is asking for something
  like a graphical or point-and-click adventure game.

Never call both tools. Do not answer without using a tool. Recommend the game
returned by the tool, and keep the final answer to one short sentence.
""".strip()


@function_tool
def recommend_text_adventure_game() -> str:
    """Return the name of a text adventure game the user has not already played."""
    return get_text_adventure_game()


@function_tool
def recommend_graphical_adventure_game() -> str:
    """Return the name of a graphical adventure game the user has not already played."""
    return get_graphical_adventure_game()


def get_agent_response(prompt: str) -> str:
    """Return the agent's final response to the user's adventure-game request."""
    agent = Agent(
        name="Adventurer Oliver",
        instructions=_INSTRUCTIONS,
        model=_MODEL_NAME,
        model_settings=ModelSettings(
            parallel_tool_calls=False,
            tool_choice="required",
        ),
        tools=[
            recommend_text_adventure_game,
            recommend_graphical_adventure_game,
        ],
    )
    result = Runner.run_sync(agent, prompt, max_turns=3)

    return result.final_output_as(str, raise_if_incorrect_type=True)
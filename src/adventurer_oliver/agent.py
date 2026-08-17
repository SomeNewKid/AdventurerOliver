"""OpenAI Agents SDK integration for Adventurer Oliver."""

from __future__ import annotations

from agents import (
    Agent,
    ModelSettings,
    RunConfig,
    Runner,
    custom_span,
    function_tool,
    trace,
)
from agents.usage import Usage
from openai.types.shared.reasoning import Reasoning

from .games import get_graphical_adventure_game, get_text_adventure_game

_MODEL_NAME = "gpt-5"

# These rates are subject to change.
# Hard-coded here for simplicity.
_INPUT_RATE_PER_1M = 1.25
_CACHED_INPUT_RATE_PER_1M = 0.125
_OUTPUT_RATE_PER_1M = 10.00

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
            reasoning=Reasoning(summary="detailed"),
        ),
        tools=[
            recommend_text_adventure_game,
            recommend_graphical_adventure_game,
        ],
    )
    with trace(
        "Adventurer Oliver",
        group_id="tool-selection-experiment-001",
        metadata={
            "app": "adventurer_oliver",
            "experiment": "tool-selection-tracing",
            "model": _MODEL_NAME,
        },
    ) as current_trace:
        result = Runner.run_sync(
            agent,
            prompt,
            max_turns=3,
            run_config=RunConfig(trace_include_sensitive_data=True),
        )

        usage = result.context_wrapper.usage

        with custom_span(
            "total_token_usage",
            data={
                "requests": usage.requests,
                "input_tokens": usage.input_tokens,
                "output_tokens": usage.output_tokens,
                "total_tokens": usage.total_tokens,
                "reasoning_tokens": usage.output_tokens_details.reasoning_tokens,
            },
        ):
            pass

        cost_details = _estimate_run_cost(usage)
        with custom_span("estimated_cost", data=cost_details):
            pass

    print(f"Trace ID: {current_trace.trace_id}")

    return result.final_output_as(str, raise_if_incorrect_type=True)


def _estimate_run_cost(usage: Usage) -> dict[str, float | int | str]:
    input_tokens = usage.input_tokens
    cached_input_tokens = usage.input_tokens_details.cached_tokens
    uncached_input_tokens = input_tokens - cached_input_tokens
    output_tokens = usage.output_tokens
    reasoning_tokens = usage.output_tokens_details.reasoning_tokens

    uncached_input_cost = _calculate_token_cost(
        uncached_input_tokens,
        _INPUT_RATE_PER_1M,
    )
    cached_input_cost = _calculate_token_cost(
        cached_input_tokens,
        _CACHED_INPUT_RATE_PER_1M,
    )
    output_cost = _calculate_token_cost(output_tokens, _OUTPUT_RATE_PER_1M)
    total_cost = uncached_input_cost + cached_input_cost + output_cost

    return {
        "model": _MODEL_NAME,
        "currency": "usd",
        "input_tokens": input_tokens,
        "cached_input_tokens": cached_input_tokens,
        "uncached_input_tokens": uncached_input_tokens,
        "output_tokens": output_tokens,
        "reasoning_tokens": reasoning_tokens,
        "input_rate_per_1m": _INPUT_RATE_PER_1M,
        "cached_input_rate_per_1m": _CACHED_INPUT_RATE_PER_1M,
        "output_rate_per_1m": _OUTPUT_RATE_PER_1M,
        "uncached_input_cost": uncached_input_cost,
        "cached_input_cost": cached_input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost,
    }


def _calculate_token_cost(tokens: int, rate_per_1m: float) -> float:
    return tokens * rate_per_1m / 1_000_000

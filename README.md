# Adventurer Oliver

Adventurer Oliver is a small Python command-line sample for exploring
observability and tracing in the OpenAI Agents SDK. It uses a deliberately
simple adventure-game recommendation agent so the trace output stays easy to
inspect.

> [!WARNING]
> This is an experimental project and should not be considered production-ready.

The project was created to take first steps with OpenAI Agents SDK tracing. The
recommendation task is intentionally secondary: the main purpose is to observe
agent runs, model turns, tool calls, custom spans, token usage, and estimated
costs in the OpenAI Traces dashboard.

## What It Does

The CLI accepts a prompt such as:

```powershell
.\.venv\Scripts\python.exe -m adventurer_oliver "An adventure game like Zork."
```

The agent then:

- sends the user's prompt to a `gpt-5` agent
- asks the model to choose exactly one recommendation tool
- calls either a text-adventure or graphical-adventure recommendation tool
- records custom trace spans for token usage and estimated cost
- prints the trace ID and the agent's final recommendation

Traces can be viewed in the OpenAI Traces dashboard:

[https://platform.openai.com/traces](https://platform.openai.com/traces)

## Tracing Focus

This project keeps the agent behavior small so tracing details are visible. A
single run can show:

- the top-level agent workflow trace
- model request spans for each turn
- reasoning summaries when enabled by model settings
- function tool call spans
- custom spans from local Python code
- total input, output, and reasoning token usage
- an estimated USD cost span based on configured `gpt-5` token rates

The custom cost span is an estimate for learning and debugging. Authoritative
billing information should come from the OpenAI usage and costs reporting tools.

## Requirements

- Python 3.11.
- PowerShell on Windows.
- An `OPENAI_API_KEY` environment variable for OpenAI model calls and tracing.

## Setup

Create the virtual environment and install the project with development
dependencies:

```powershell
.\scripts\setup-dev.ps1
```

The setup script expects Python 3.11 at the path configured in
`scripts\setup-dev.ps1`.

## Running

Run the tracing sample from the repository root:

```powershell
.\.venv\Scripts\python.exe -m adventurer_oliver "An adventure game like Zork."
```

You can also try a graphical adventure prompt:

```powershell
.\.venv\Scripts\python.exe -m adventurer_oliver "An adventure game like King's Quest."
```

The command prints the trace ID before the final recommendation. Use that trace
ID to find the run in the OpenAI Traces dashboard.

## Development Checks

Run formatting, linting, type checking, and tests:

```powershell
.\scripts\check.ps1
```

This runs:

- `ruff format .`
- `ruff check .`
- `pyright`
- `pytest`

## Project Structure

```text
src/adventurer_oliver/
  __main__.py  Package entry point for python -m adventurer_oliver
  cli.py       Command-line entry point
  agent.py     OpenAI Agents SDK setup, tool definitions, tracing, and cost spans
  games.py     Local recommendation helpers used by the tools

tests/
  test_smoke.py

scripts/
  setup-dev.ps1
  check.ps1
```

## Notes

This project is an observability learning exercise, not a general-purpose game
recommendation system. The game lists are hard-coded, and the recommendation
tools return random local choices.

Agent behavior, tool selection, reasoning summaries, and final wording can vary
between runs because the workflow is model-driven. OpenAI API calls may incur
usage costs.

The estimated-cost trace span uses hard-coded token prices for simplicity. Check
current OpenAI pricing before relying on those values for anything beyond local
experimentation.

## Third-Party Notices

This project has a direct runtime dependency on the `openai-agents` Python
package (MIT). See the package's PyPI license metadata for full license and
notice terms.

## License

GNU General Public License v3.0. See the `LICENSE` file for details.

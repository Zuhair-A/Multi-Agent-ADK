# ADK Utility Assistant

Small Agent Development Kit (ADK) app that exposes a single LLM agent with a few utility tools:

- General chat / greetings
- Current date/time
- Stock price lookup (via `yfinance`)

## Prerequisites

- Python 3.12+ (this repo pins `3.12` in `.python-version`)
- Recommended: `uv` (this repo includes `uv.lock`)
- If you use the default model: Ollama running locally
  - The agent is configured for `ollama_chat/llama3.2:latest`

## Setup

Using `uv` (recommended):

```bash
uv sync
```

(Alternative) Using `pip`:

```bash
python -m venv .venv
# PowerShell
.\.venv\Scripts\Activate.ps1

pip install "dotenv>=0.9.9" "google-adk>=2.0.0" "google-cloud-resource-manager>=1.17.0" "litellm>=1.85.0" "ollama>=0.6.2" "openai>=2.37.0" "yfinance>=1.3.0"
```

## Run

If you’re using the default Ollama-backed model, ensure the model is available:

```bash
ollama pull llama3.2:latest
```

### CLI (interactive)

From the repo root:

```bash
adk run app
```

Single-shot query:

```bash
adk run app "What time is it?"
adk run app "AAPL stock price"
```

### Web UI

Serve a simple web UI for any agents under the provided directory. This repo has one agent folder: `app/`.

```bash
adk web .
```

Optional port:

```bash
adk web --port 8000 .
```

## Model configuration

The model is set in `app/agent.py`:

- Default: `LiteLlm(model="ollama_chat/llama3.2:latest")`

To use a different provider/model, update that string and set any required environment variables for LiteLLM.

## Project layout

- `app/agent.py`: agent + tool implementations; exports `root_agent`
- `app/__init__.py`: package init (imports `agent`)

## Notes

- Do not commit local environments (e.g. `.venv/`).
- If you store secrets in an `.env` file, keep it untracked.

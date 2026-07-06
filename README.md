# BrowserUse

A minimal Python project that uses the [`browser-use`](https://github.com/browser-use/browser-use) library to run LLM-powered agents that control a real Chrome browser. Includes both a CLI script and a Gradio web UI.

## Features

- 🖥️ **CLI runner** (`main.py`) — run a quick agent task from the terminal
- 🌐 **Web UI** (`webui.py`) — a Gradio interface for running arbitrary browser tasks interactively, with model selection, max-step control, and an optional API key field
- 🔑 Reads your OpenAI API key from a `.env` file (or lets you paste one directly in the UI)

## Requirements

- Python 3.12+
- Google Chrome
- An OpenAI API key (or another supported LLM provider key)

## Setup

```powershell
# Clone the repo
git clone https://github.com/FlameFragger414/BrowserUse.git
cd BrowserUse

# Create and activate a virtual environment
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Configure your API key
copy .env.example .env
# then edit .env and set OPENAI_API_KEY=your-key-here
```

## Usage

### CLI

Runs a single hardcoded task (edit `main.py` to change the task or model):

```powershell
python main.py
```

### Web UI

Launches a local Gradio app for running arbitrary tasks:

```powershell
python webui.py
```

Then open [http://127.0.0.1:7860](http://127.0.0.1:7860) in your browser. From the UI you can:

- Enter a free-text task (e.g. *"Find the number 1 post on Show HN"*)
- Choose a model (`gpt-5-nano`, `gpt-5-mini`, `gpt-5`, `gpt-4.1-mini`, `gpt-4.1`, `gpt-4o`, `o4-mini`, `o3`)
- Set a max step count (5–100)
- Optionally paste an API key (falls back to `OPENAI_API_KEY` from `.env` if left blank)

## Browser Connection Requirement

`browser-use` connects to a real Chrome instance via the Chrome DevTools Protocol (CDP):

1. Make sure Chrome is running.
2. Enable remote debugging: open `chrome://inspect/#remote-debugging` and turn on **"Allow remote debugging for this browser instance"**.
3. Diagnose connection issues anytime with:
   ```powershell
   .\.venv\Scripts\browser-use.exe --doctor
   ```

## Project Structure

| Path | Purpose |
|---|---|
| `main.py` | CLI entry point — runs a single hardcoded agent task |
| `webui.py` | Gradio web UI for running arbitrary tasks interactively |
| `requirements.txt` | Pinned dependencies |
| `.env.example` | Template for `.env` — shows supported key names |
| `.gitignore` | Ignores `.venv/`, `.env`, caches, logs |

## Configuration

`.env.example` documents the supported environment variables:

```
OPENAI_API_KEY=          # used by main.py and webui.py

# Or use another provider:
# BROWSER_USE_API_KEY=
# GOOGLE_API_KEY=
# ANTHROPIC_API_KEY=
```

> Note: only OpenAI is currently wired up in code. To use another provider, import the matching chat class from `browser_use` (e.g. `ChatAnthropic`, `ChatGoogle`) and set the corresponding API key.

## License

No license specified yet.

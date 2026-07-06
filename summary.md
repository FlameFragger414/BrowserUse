# BrowserUse Project Summary

A minimal Python project that uses the [`browser-use`](https://github.com/browser-use/browser-use) library to run
LLM-powered agents that control a real Chrome browser. Includes both a CLI script and a Gradio web UI.

## Folder Contents

| Path | Type | Purpose |
|---|---|---|
| `main.py` | Script | CLI entry point — runs a single hardcoded agent task |
| `webui.py` | Script | Gradio web UI for running arbitrary tasks interactively |
| `requirements.txt` | Config | Pinned dependencies |
| `.env` | Config (gitignored) | Holds `OPENAI_API_KEY` (currently set) |
| `.env.example` | Config | Template for `.env` — shows supported key names |
| `.gitignore` | Config | Ignores `.venv/`, `.env`, caches, logs |
| `.venv/` | Environment | Python 3.12.0 virtual environment with all dependencies installed |

## Environment

- **Python:** 3.12.0 (via `.venv`, created with `py -3.12 -m venv .venv`)
- **Activate:** `.\.venv\Scripts\Activate.ps1` (PowerShell)
- **Key installed packages:**
  - `browser-use` 0.13.3 — core agent/browser automation library
  - `browser-use-sdk` 3.4.2 — SDK companion package
  - `gradio` 6.19.0 + `gradio_client` 2.5.0 — web UI framework
  - `python-dotenv` 1.2.2 — loads `.env` into environment variables
  - Plus transitive deps: `openai`, `anthropic`, `google-genai`, `playwright`-adjacent browser harness (`browser-harness`), `pydantic`, `rich`, `mcp`, etc.

## `.env` / `.env.example`

- `.env.example` documents supported keys: `OPENAI_API_KEY` (primary, used by both scripts), plus commented-out alternatives (`BROWSER_USE_API_KEY`, `GOOGLE_API_KEY`, `ANTHROPIC_API_KEY`).
- `.env` currently has `OPENAI_API_KEY` **set** (value not inspected/exposed here). No other keys are configured.

## `main.py` — CLI Script

```python
llm = ChatOpenAI(model="gpt-5-nano")
task = "Find the number 1 post on Show HN"
agent = Agent(task=task, llm=llm)
await agent.run()
```

- Loads `.env` via `python-dotenv`.
- Hardcoded single task, hardcoded model (`gpt-5-nano`).
- Run with: `python main.py` (after activating `.venv`).
- No output formatting — relies on `browser-use`'s default console logging.

## `webui.py` — Gradio Web UI

- Launches locally at `http://127.0.0.1:7860` via `python webui.py`.
- UI fields:
  - **Task** — free-text description of what the agent should do
  - **Model** — dropdown, defaults to `gpt-5-nano`; also offers `gpt-5-mini`, `gpt-5`, `gpt-4.1-mini`, `gpt-4.1`, `gpt-4o`, `o4-mini`, `o3`
  - **Max steps** — slider, 5–100, default 25
  - **OpenAI API key** — optional password field; falls back to `OPENAI_API_KEY` from `.env` if left blank
  - **Result** — read-only output box showing the agent's final result (or step-by-step extracted content if no single final result is available)
- Sets `asyncio.WindowsProactorEventLoopPolicy()` on Windows (`os.name == "nt"`) for compatibility with subprocess-based browser control.
- Wraps `agent.run()` in a helper (`_format_result`) that prefers `history.final_result()` and falls back to concatenated `history.extracted_content()`.
- Runs the async agent task via `asyncio.run(...)` inside the Gradio click handler (synchronous bridge).

## How to Run

```powershell
cd d:\BrowserUse
.\.venv\Scripts\Activate.ps1

# CLI version
python main.py

# Web UI version
python webui.py   # then open http://127.0.0.1:7860
```

## Browser Connection Requirement

Both scripts rely on `browser-use` connecting to a real Chrome instance via CDP (Chrome DevTools Protocol):

1. Chrome must be running.
2. Remote debugging must be allowed: open `chrome://inspect/#remote-debugging` and enable **"Allow remote debugging for this browser instance"**.
3. Diagnose connection issues anytime with:
   ```powershell
   .\.venv\Scripts\browser-use.exe --doctor
   ```

## Notable Gaps / Things Not Yet Set Up

- No `.git` repository initialized yet (only a `.gitignore` exists).
- No automated tests.
- No logging/history persistence (e.g. `AgentHistoryList.save_to_file(...)` is available in the library but unused).
- `main.py` task/model are hardcoded — no CLI args or config file for changing them without editing code.
- Only OpenAI is wired up; `.env.example` lists other providers (Google, Anthropic, Browser Use Cloud) but no code path currently uses them.
- No Docker/production deployment setup — this is a local dev-only setup.

## Quick Reference: Changing Behavior

| Want to... | Edit |
|---|---|
| Change the CLI task | `main.py` → `task` variable |
| Change the CLI model | `main.py` → `ChatOpenAI(model=...)` |
| Add a model choice to the web UI | `webui.py` → `MODEL_CHOICES` list |
| Switch LLM provider | Import a different chat class from `browser_use` (e.g. `ChatAnthropic`, `ChatGoogle`) and set the matching API key in `.env` |
| Change web UI port/host | `webui.py` → `create_ui().launch(server_name=..., server_port=...)` |

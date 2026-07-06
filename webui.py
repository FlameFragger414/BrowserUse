import asyncio
import os

from dotenv import load_dotenv

load_dotenv()

import gradio as gr
from browser_use import Agent, ChatOpenAI

if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

DEFAULT_MODEL = "gpt-5-nano"
MODEL_CHOICES = [
    "gpt-5-nano",
    "gpt-5-mini",
    "gpt-5",
    "gpt-4.1-mini",
    "gpt-4.1",
    "gpt-4o",
    "o4-mini",
    "o3",
]


def _format_result(history) -> str:
    final = history.final_result()
    if final:
        return final

    lines: list[str] = []
    for step, content in enumerate(history.extracted_content(), start=1):
        lines.append(f"Step {step}:\n{content}")

    if lines:
        return "\n\n".join(lines)

    return str(history)


async def run_browser_task(
    task: str,
    model: str,
    api_key: str,
    max_steps: int,
) -> str:
    if not task.strip():
        return "Please enter a task."

    key = api_key.strip() or os.getenv("OPENAI_API_KEY", "")
    if not key:
        return "Set OPENAI_API_KEY in .env or paste your key above."

    os.environ["OPENAI_API_KEY"] = key

    try:
        agent = Agent(
            task=task.strip(),
            llm=ChatOpenAI(model=model),
        )
        history = await agent.run(max_steps=max_steps)
        return _format_result(history)
    except Exception as e:
        return f"Error: {e}"


def create_ui() -> gr.Blocks:
    env_key_set = bool(os.getenv("OPENAI_API_KEY"))

    with gr.Blocks(title="Browser Use") as interface:
        gr.Markdown(
            "# Browser Use\n"
            "Describe a web task and the agent will run it in your browser."
        )

        with gr.Row():
            with gr.Column(scale=1):
                task = gr.Textbox(
                    label="Task",
                    placeholder="e.g. Find the number 1 post on Show HN",
                    lines=4,
                )
                model = gr.Dropdown(
                    choices=MODEL_CHOICES,
                    value=DEFAULT_MODEL,
                    label="Model",
                )
                max_steps = gr.Slider(
                    minimum=5,
                    maximum=100,
                    value=25,
                    step=1,
                    label="Max steps",
                )
                api_key = gr.Textbox(
                    label="OpenAI API key (optional)",
                    placeholder="Uses OPENAI_API_KEY from .env if left blank",
                    type="password",
                    value="" if env_key_set else "",
                )
                submit_btn = gr.Button("Run", variant="primary")

            with gr.Column(scale=1):
                output = gr.Textbox(
                    label="Result",
                    lines=20,
                    interactive=False,
                )

        submit_btn.click(
            fn=lambda *args: asyncio.run(run_browser_task(*args)),
            inputs=[task, model, api_key, max_steps],
            outputs=output,
        )

    return interface


if __name__ == "__main__":
    create_ui().launch(server_name="127.0.0.1", server_port=7860)

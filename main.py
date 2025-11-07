import src.config # noqa: F401

import os
import glob
import shutil
import traceback
from json import dumps, loads
from datetime import datetime

import aiofiles

from src.agents.prompts import USER_PROMPT
from src.agents.simple import simple # noqa: F401
from src.agents.intent import intent # noqa: F401
from src.tools import CONTENT_DIR, RUN_ID


async def cleanup():
    if os.path.exists(CONTENT_DIR):
        shutil.rmtree(CONTENT_DIR, ignore_errors=True)
        print(f"Removed existing content directory at: {CONTENT_DIR}")

    for file in glob.glob("/tmp/agent-ctx__*"):
        os.remove(file)

async def copy_outcome_to_final(final_path: str, metrics_path: str):
    async with aiofiles.open(final_path, "r") as f:
        final = loads(await f.read())

    final["metrics"] = {}

    if os.path.exists(metrics_path):
        async with aiofiles.open(metrics_path, "r") as f:
            metrics = loads(await f.read())
            final["metrics"] = metrics

    else:
        print(f"Metrics file not found at: {metrics_path}")

    async with aiofiles.open(final_path, "w") as f:
        await f.write(dumps(final, indent=2))

async def main():
    # model_name = "anthropic/claude-sonnet-4.5"
    # model_name = "openai/gpt-4.1-mini"
    # model_name = "openai/gpt-4o"
    # model_name = "google/gemini-2.5-flash-preview-09-2025"
    model_name = "google/gemini-2.5-pro"

    # user_prompt = "Just the total rides in januray"
    user_prompt = USER_PROMPT

    metrics_path = os.path.join(
        CONTENT_DIR,
        "efficiency_metrics.json"
    )

    os.makedirs("outputs", exist_ok=True)

    final_output_dir = os.path.join("outputs", RUN_ID)
    os.makedirs(final_output_dir, exist_ok=True)

    print(f"Using model: {model_name} and run ID: {RUN_ID}")

    try:
        await cleanup()
        final_path = await simple(
            model_name=model_name,
            use_summarization=False,
            user_prompt=user_prompt
        )

        await copy_outcome_to_final(
            final_path,
            metrics_path,
        )

    except Exception as e:
        print(f"Error: {e}\n{traceback.format_exc()}")

    try:
        await cleanup()

        final_path = await simple(
            model_name=model_name,
            use_summarization=True,
            user_prompt=user_prompt
        )

        await copy_outcome_to_final(
            final_path,
            metrics_path,
        )

    except Exception as e:
        print(f"Error: {e}\n{traceback.format_exc()}")

    try:
        await cleanup()

        final_path = await intent(
            model_name=model_name,
            user_prompt=user_prompt
        )

        await copy_outcome_to_final(
            final_path,
            metrics_path,
        )

    except Exception as e:
        print(f"Error: {e}\n{traceback.format_exc()}")


if __name__ == "__main__":
    import asyncio

    for i in range(3):
        RUN_ID = datetime.now().strftime("%Y%m%dT%H%M%S")
        asyncio.run(main())

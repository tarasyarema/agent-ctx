import src.config # noqa: F401

import os
import glob
import shutil
import traceback

from src.agents.simple import simple
from src.tools import CONTENT_DIR


async def main():
    if os.path.exists(CONTENT_DIR):
        shutil.rmtree(CONTENT_DIR, ignore_errors=True)
        print(f"Removed existing content directory at: {CONTENT_DIR}")

    for file in glob.glob("/tmp/agent-ctx__*"):
        os.remove(file)

    try:
        await simple(
            use_summarization=False
        )

    except Exception as e:
        print(f"Error: {e}\n{traceback.format_exc()}")



if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

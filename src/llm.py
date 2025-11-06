import os

from langchain_openai import ChatOpenAI
from pydantic import SecretStr


def new_llm(model_name: str):
    OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]

    return ChatOpenAI(
        api_key=SecretStr(OPENROUTER_API_KEY),
        base_url="https://openrouter.ai/api/v1",
        model=model_name,
        timeout=60,
        temperature=0.0,
        max_retries=3,
    )

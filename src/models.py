from pydantic import BaseModel


MODELS = {
    "gem-flash": "google/gemini-2.5-flash-preview-09-2025",
    "gem-pro": "google/gemini-2.5-pro",
    "ant-sonnet": "anthropic/claude-sonnet-4.5",
    "ant-haiku": "anthropic/claude-haiku-4.5",
    "oai-5-mini": "openai/gpt-5-mini",
    "oai-4.1-mini": "openai/gpt-4.1-mini",
    "oai-4o": "openai/gpt-4o",
}


class Reference(BaseModel):
    text: str
    link: str | None = None
    filename: str | None = None
    sql_query: str | None = None


class FinalResponse(BaseModel):
    text: str
    references: list[Reference] = []

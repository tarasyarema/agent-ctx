import os
import httpx

from aiofiles import open as aio_open
from langchain_core.messages import UsageMetadata
from pydantic import BaseModel


PRICING_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "models.json",
)

class ModelPricing(BaseModel):
    prompt: float  # cost per input token in USD
    completion: float  # cost per output token in USD
    internal_reasoning: float | None = 0.0
    input_cache_read: float | None = 0.0
    input_cache_write: float | None = 0.0

    model_config = {
        "arbitrary_types_allowed": True,
    }

class ModelInfo(BaseModel):
    id: str
    pricing: ModelPricing

    model_config = {
        "arbitrary_types_allowed": True,
    }


class ModelPrices(BaseModel):
    data: list[ModelInfo]


class UsagePrice(BaseModel):
    input_cost: float  # in USD

    input_cache_read_cost: float | None = 0.0  # in USD
    input_cache_write_cost: float | None = 0.0  # in USD
    input_cache_total_cost: float | None = 0.0  # in USD

    output_cost: float  # in USD

    input_total_cost: float
    output_total_cost: float
    total_cost: float  # in USD


async def _read_model_prices() -> ModelPrices:
    async with aio_open(PRICING_PATH, "r") as f:
        content = await f.read()
        model_prices = ModelPrices.model_validate_json(content)

    return model_prices


async def compute_cost(model_name: str, usage: UsageMetadata, openrouter: bool = True) -> UsagePrice:
    prices = await _read_model_prices()
    _model_name = model_name

    model_price = next(
        (m for m in prices.data if m.id == _model_name),
        None,
    )

    if model_price is None:
        raise ValueError(f"Unknown model for pricing: {_model_name}")

    input_cost = usage["input_tokens"] * model_price.pricing.prompt

    input_cache_read_cost = (usage.get("input_token_details", {}).get("cache_read") or 0) * (model_price.pricing.input_cache_read or 0.0)
    input_cache_write_cost = (usage.get("input_token_details", {}).get("cache_creation") or 0) * (model_price.pricing.input_cache_write or 0.0)
    input_cache_total_cost = input_cache_read_cost + input_cache_write_cost

    output_cost = usage["output_tokens"] * model_price.pricing.completion

    total_cost = input_cost + output_cost

    return UsagePrice(
        input_cost=input_cost,
        input_cache_read_cost=input_cache_read_cost,
        input_cache_write_cost=input_cache_write_cost,
        input_cache_total_cost=input_cache_total_cost,

        output_cost=output_cost,
        output_total_cost=output_cost,

        input_total_cost=input_cost + input_cache_total_cost,
        total_cost=total_cost,
    )


from datetime import datetime, timezone
from json import dumps
import aiofiles
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, UsageMetadata
from langchain_core.callbacks import UsageMetadataCallbackHandler
from langchain.agents.structured_output import ToolStrategy
from langchain.agents.middleware import SummarizationMiddleware
from langchain_core.messages.utils import count_tokens_approximately


from src.agents.prompts import USER_PROMPT
from src.agents.simple_prompts import CUSTOM_SUMMARY_PREFIX, CUSTOM_SUMMARY_PROMPT, SYSTEM_PROMPT
from src.cost import compute_cost
from src.llm import new_llm
from src.models import MODELS, FinalResponse
from src.tools import RUN_ID, get_tools


async def simple(
    user_prompt: str = USER_PROMPT,
    use_summarization: bool = False, 
    model_name: str | None = None
):
    print(f"Starting simple agent with summarization={use_summarization}")

    _model_name = model_name or MODELS["ant-haiku"]
    llm = new_llm(_model_name)

    agent = create_agent(
        model=llm,
        tools=get_tools(),
        system_prompt=SYSTEM_PROMPT,
        response_format=ToolStrategy(FinalResponse),
        debug=False,
        middleware=[
            SummarizationMiddleware(
                model=new_llm("openai/gpt-4o-mini"),
                max_tokens_before_summary=12000,
                messages_to_keep=20,
                summary_prompt=CUSTOM_SUMMARY_PROMPT,
                summary_prefix=CUSTOM_SUMMARY_PREFIX,
            )
        ] if use_summarization else [],
    )

    output: FinalResponse | None = None

    callback = UsageMetadataCallbackHandler()

    meta_usages: list[UsageMetadata] = []
    latencies: list[dict[str, str | float]] = []
    tokens_used: list[int] = []

    msg_count = 0

    chunk = None

    start = datetime.now(timezone.utc)
    _start_time = start

    try:
        async for chunk in agent.astream(
            {
                "messages": [
                    HumanMessage(
                        content=user_prompt
                    )
                ]
            },
            stream_mode="values",
            config={
                "recursion_limit": 100,
                "callbacks": [callback]
            }
        ):
            msg_count += 1

            # Each chunk contains the full state at that point
            latest_message = chunk["messages"][-1]

            _now = datetime.now(timezone.utc)
            elapsed = _now - start

            latencies.append({
                "iteration": len(latencies) + 1,
                "start": start.isoformat(),
                "end": _now.isoformat(),
                "elapsed_seconds": elapsed.total_seconds()
            })

            start = _now

            try:
                estimated_tokens = count_tokens_approximately(chunk["messages"])

            except Exception as e:
                print(f"Error estimating tokens: {e}")
                estimated_tokens = -1

            tokens_used.append(estimated_tokens)

            print(f"Iteration {msg_count} with {len(chunk['messages'])} took {elapsed.total_seconds():.2f} seconds with ~{estimated_tokens} tokens")

            if "structured_response" in chunk:
                print("\nStructured Response Update:")
                output = chunk["structured_response"]

            if latest_message.content:
                print(f"Agent:\n{latest_message.content}")

                if _model_name in callback.usage_metadata:
                    meta_usages.append(callback.usage_metadata[_model_name])

            elif hasattr(latest_message, "tool_calls") and latest_message.tool_calls:
                print(f"Calling tools: {[tc['name'] for tc in latest_message.tool_calls]}")

    except Exception as e:
        print(f"Error during agent execution: {e}")

    if output:
        print("\nFinal Response:")
        print(output.model_dump_json(indent=2))

    print("\n\n----\n")
    print(dumps(callback.usage_metadata, indent=2))

    for model, usage in callback.usage_metadata.items():
        _cost = await compute_cost(model, usage)
        print(_cost.model_dump_json(indent=2))

    print(f"{msg_count} total messages exchanged")

    _data = {
        "run_id": RUN_ID,
        "total_messages": msg_count,
        "tokens": callback.usage_metadata,
        "costs": {
            model: (await compute_cost(model, usage)).model_dump()
            for model, usage in callback.usage_metadata.items()
        },
        "tokens_details": meta_usages,
        "final_output": output.model_dump() if output else None,
        "summarization_used": use_summarization,
        "agent_type": "simple",
        "latencies": latencies,
        "start_time": _start_time.isoformat(),
        "end_time": datetime.now(timezone.utc).isoformat(),
        "total_time_seconds": sum(float(l["elapsed_seconds"]) for l in latencies),
        "tokens_used_approx": tokens_used,
    }

    _model_name_norm = _model_name.replace("/", "-").replace(" ", "_")
    _final_path = f"outputs/{RUN_ID}/{_model_name_norm}-simple-{'summarization' if use_summarization else 'raw'}.json"

    async with aiofiles.open(_final_path, "w") as f:
        await f.write(dumps(_data, indent=2))

    print(f"Wrote full run data to {_final_path}")
    return _final_path

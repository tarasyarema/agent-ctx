from datetime import datetime, timezone
from json import dumps
from typing import Annotated, Any, Literal
import aiofiles
from langchain.tools import BaseTool
from langchain_core.messages import HumanMessage, SystemMessage, UsageMetadata
from langchain_core.messages.utils import count_tokens_approximately
from pydantic import BaseModel, Field, create_model
from src.agents.intent_prompts import build_dynamic_system_prompt
from src.agents.prompts import USER_PROMPT
from src.cost import UsagePrice, compute_cost, sum_prices, sum_tokens
from src.llm import new_llm
from src.models import MODELS, FinalResponse
from src.tools import RUN_ID, get_tools


Status = Literal["pending", "completed", "failed"]


class NoOpArgs(BaseModel):
    """No operation arguments."""
    pass

class BaseIntent(BaseModel):
    reasoning: str = Field(
        ...,
        description="The reasoning behind choosing this intent.",
    )

    previous_step_analysis: str = Field(
        ...,
        description="Brief and concise analysis of the previous step's outcome.",
    )

    next_task: str | None = Field(
        None,
        description="Single sentence description of the next task to be performed based on this intent, if applicable.",
    )

    memory: str | None = Field(
        None,
        description="Relevant memory or context to preserve for future steps. Use carefully to avoid exceeding token limits.",
    )


class StepIntent(BaseIntent):
    type: str
    args: Any

    output: str | Any | None = None

    status: Status = "pending"
    error_message: str | None = None


class Timing(BaseModel):
    started_at: datetime
    ended_at: datetime | None = None
    elapsed_seconds: float | None = None

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        if self.started_at:
            data["started_at"] = self.started_at.isoformat()
        if self.ended_at:
            data["ended_at"] = self.ended_at.isoformat()
        return data


class AgentHistoryStep(Timing):
    tokens_used_approx: int
    tokens_used: UsageMetadata | None = None

    cost: UsagePrice | None = None

    status: Status = "pending"

    intents: list[StepIntent] = []




class ClarificationIntent(BaseModel):
    """
    Intent to ask for clarification from the user.
    """

    step_index: int = Field(
        ...,
        description="The index of the step in the agent history that requires clarification.",
    )


class FinalResponseIntent(BaseModel):
    """
    Intent to ask for clarification from the user.
    """

    status: Status = Field(
        ...,
        description="The status of the final response intent, should be 'completed' when the final response is ready, and failed if there was an error.",
    )

    response: FinalResponse = Field(
        ...,
        description="The final response data to return to the user, once the agent has completed its task.",
    )


def create_intent_model(mdl: type[BaseModel], doc: str | None = None) -> type[BaseModel]:
    m = create_model(
        f"{mdl.__name__}_Intent",
        type=(
            Annotated[
                Literal[mdl.__name__], 
                Field(
                    default=mdl.__name__,
                    title="Intent Type `type`",
                    description=f"The type of intent being invoked, should be '{mdl.__name__}'.",
                )
            ]
        ),
        intent_args=(
            Annotated[
                mdl,
                Field(
                    ...,
                    title="Intent Arguments `intent_args`",
                    description=doc or mdl.__doc__ or f"The arguments for the {mdl.__name__}.",
                )
            ]
        ),
        __base__=BaseIntent,
    )

    m.__doc__ = f"Intent model for {doc or mdl.__name__}."

    return m


class AgentHistory(Timing):
    run_id: str
    model_name: str

    user_prompt: str

    steps: list[AgentHistoryStep] = []
    final_response: FinalResponse | None = None

    current_messages: list[str] = []


async def persist_agent(agent: AgentHistory):
    _data = {
        "run_id": RUN_ID,
        "total_messages": len(agent.steps),
        "tokens": {
            agent.model_name: sum_tokens([
                step.tokens_used
                for step in agent.steps
                if step.tokens_used is not None
            ])
        },
        "costs": {
            agent.model_name: sum_prices([
                step.cost
                for step in agent.steps
                if step.cost is not None
            ]).model_dump()
        },
        "tokens_details": [
            step.tokens_used
            for step in agent.steps
            if step.tokens_used is not None
        ],
        "final_output": agent.final_response.model_dump() if agent.final_response else None,
        "summarization_used": False,
        "agent_type": "intent",
        "latencies": [
            {
                "iteration": idx + 1,
                "start": step.started_at.isoformat(),
                "end": step.ended_at.isoformat() if step.ended_at else None,
                "elapsed_seconds": step.elapsed_seconds
            }
            for idx, step in enumerate(agent.steps)
        ],
        "start_time": agent.started_at.isoformat(),
        "end_time": agent.ended_at.isoformat() if agent.ended_at else None,
        "total_time_seconds": agent.elapsed_seconds,
        "tokens_used_approx": [
            step.tokens_used_approx
            for step in agent.steps
        ],
        "agent_steps": [
            step.model_dump()
            for step in agent.steps
        ],
    }

    _model_name_norm = agent.model_name.replace("/", "-").replace(" ", "_")
    _final_path = f"outputs/{agent.run_id}/{_model_name_norm}-intent.json"

    async with aiofiles.open(_final_path, "w") as f:
        await f.write(dumps(_data, indent=2))

    print(f"Persisted (intent) agent history to {_final_path}")
    return _final_path


MAX_ITS = 100

async def intent(
    user_prompt: str = USER_PROMPT,
    model_name: str | None = None
):
    print("Starting intent-based agent")

    _model_name = model_name or MODELS["ant-haiku"]
    llm = new_llm(_model_name)

    agent = AgentHistory(
        run_id=RUN_ID,
        model_name=_model_name,
        started_at=datetime.now(timezone.utc),
        user_prompt=user_prompt,
    )

    _default_tools = get_tools()
    _default_tool_names = [t.input_schema.__name__ for t in _default_tools]

    it = 0
    should_exit = False  # Flag to signal completion

    _llm_tools: list[type[BaseModel]] = [
        create_intent_model(ClarificationIntent),
        create_intent_model(FinalResponseIntent),
    ]

    for t in _default_tools:
        _llm_tools.append(
            create_intent_model(
                t.input_schema,
                t.description
            )
        )

    llm = llm.bind_tools(
        tools=_llm_tools,
        strict=True,
        parallel_tool_calls=True,
        tool_choice="required",
    )

    while True:
        if it >= MAX_ITS:
            print(f"Reached maximum iterations of {MAX_ITS}, exiting.")
            break

        start_it = datetime.now(timezone.utc)
        it += 1

        step = AgentHistoryStep(
            started_at=start_it,
            intents=[],
            tokens_used_approx=0,
        )

        system_prompt = build_dynamic_system_prompt(
            agent=agent,
            tools=_llm_tools,
            user_prompt=user_prompt
        )

        msgs = [
            SystemMessage(content=system_prompt),
            *[
                HumanMessage(content=msg)
                for msg in agent.current_messages
            ],
            HumanMessage(
                content=f"Please decide on the next action to take."
            )
        ]


        try:
            resp = await llm.ainvoke(
                input=msgs
            )

        except Exception as e:
            print(f"Exception during LLM invocation: {str(e)}")

            step.status = "failed"

            step.ended_at = datetime.now(timezone.utc)
            step.elapsed_seconds = (step.ended_at - step.started_at).total_seconds()

            agent.current_messages.append(f"Error: Exception during LLM invocation:\n{str(e)}")
            agent.steps.append(step)

            continue

        agent.current_messages = []

        end_it = datetime.now(timezone.utc)
        elapsed = end_it - start_it

        estimated_tokens = count_tokens_approximately([
            *msgs,
            resp
        ])

        print(f"Iteration {it} with {len(agent.steps)} messages took {elapsed.total_seconds():.2f} seconds with ~{estimated_tokens} tokens (returned {len(resp.tool_calls)} tool calls)")

        if len(resp.tool_calls) == 0:
            print(resp)

            step.status = "failed"

            step.ended_at = datetime.now(timezone.utc)
            step.elapsed_seconds = (step.ended_at - step.started_at).total_seconds()

            agent.current_messages.append("Error: No tool call returned by the model.")
            agent.steps.append(step)

            continue

        for tool_call in resp.tool_calls:
            try:
                intent_type = tool_call["name"].split("_Intent")[0]
                intent_args = tool_call["args"]

                raw_intent = BaseIntent.model_validate({
                    "reasoning": intent_args.get("reasoning", ""),
                    "previous_step_analysis": intent_args.get("previous_step_analysis", ""),
                    "next_task": intent_args.get("next_task", None),
                    "memory": intent_args.get("memory", None),
                })

                intent_args = intent_args.get("intent_args", {})

                print(f"Processing intent of type: {intent_type}")

                args: BaseModel | None = None
                output: str | BaseModel | None = None
                status: Status = "completed"

                if intent_type in _default_tool_names:
                    _tool: BaseTool | None = None

                    for t in _default_tools:
                        if t.input_schema.__name__ == intent_type:
                            _tool = t
                            break

                    if _tool is None:
                        raise ValueError(f"Could not find tool for intent type: {intent_type}")

                    print(f"Executing tool for intent type: {intent_type}")

                    args = _tool.input_schema.model_validate(intent_args)
                    output = await _tool.arun(intent_args)

                    agent.current_messages.append(f"Tool '{intent_type}' executed with output:\n{output}")

                elif intent_type == "ClarificationIntent":
                    print("Processing ClarificationIntent")

                    args = ClarificationIntent.model_validate(intent_args)
                    output = None

                    if args.step_index - 1 < 0 or args.step_index - 1 >= len(agent.steps):
                        raise ValueError(f"Invalid step index for clarification: {args.step_index}")

                    step_output = agent.steps[args.step_index - 1].intents

                    step_output_str = ""

                    for intent in step_output:
                        step_output_str += f"- Intent Type: {intent.type}\n"
                        step_output_str += f"  Args: {intent.args.model_dump_json()}\n"
                        step_output_str += f"  Output: {intent.output}\n"
                        step_output_str += f"  Status: {intent.status}\n"
                        if intent.error_message:
                            step_output_str += f"  Error Message: {intent.error_message}\n"

                    agent.current_messages.append(
                        f"Here are the details of step {args.step_index} that require clarification:\n{step_output_str}"
                    )

                elif intent_type == "FinalResponseIntent":
                    print("Processing FinalResponseIntent, preparing to exit.")

                    args = FinalResponseIntent.model_validate(intent_args)
                    output = None

                    agent.final_response = args.response

                    # Signal that we should exit the main loop
                    should_exit = True

                else:
                    raise ValueError(f"Unhandled intent type: {intent_type}")

                intent = StepIntent(
                    type=intent_type,
                    args=args,
                    output=output,
                    status=status,
                    reasoning=raw_intent.reasoning,
                    previous_step_analysis=raw_intent.previous_step_analysis,
                    memory=raw_intent.memory,
                    next_task=raw_intent.next_task,
                )

                step.intents.append(intent)

            except Exception as e:
                print(f"Exception during intent processing\n{tool_call}\nError:\n{str(e)}")

                intent = StepIntent(
                    reasoning="",
                    previous_step_analysis="",
                    type=tool_call["name"],
                    args=NoOpArgs(),
                    output=None,
                    status="failed",
                    error_message=f"Exception during intent processing: {str(e)}"
                )

                step.intents.append(intent)

        step.tokens_used_approx = estimated_tokens
        step.tokens_used = resp.usage_metadata

        output_tokens = count_tokens_approximately([resp])

        step.cost = await compute_cost(
            _model_name,
            {
                "input_tokens": estimated_tokens,
                "output_tokens": output_tokens,
                "total_tokens": estimated_tokens,
            }
        )

        step.status = "failed" if any(
            intent.status == "failed"
            for intent in step.intents
        ) else "completed"

        step.ended_at = end_it
        step.elapsed_seconds = elapsed.total_seconds()

        agent.steps.append(step)

        if should_exit or agent.final_response is not None:
            break

    agent.ended_at = datetime.now(timezone.utc)
    agent.elapsed_seconds = (agent.ended_at - agent.started_at).total_seconds()

    return await persist_agent(agent)

from typing import Any
from langchain.tools import BaseTool
from pydantic import BaseModel


def truncate(output: str | Any | None, max_lines: int = 3) -> str:
    """Truncate output to first few lines with indicator for full version."""
    if output is None:
        return "None"

    # Convert to string
    if isinstance(output, BaseModel):
        output_str = output.model_dump_json(indent=2)

    elif isinstance(output, str):
        output_str = output

    else:
        output_str = str(output)

    lines = output_str.split('\n')

    if len(lines) <= max_lines:
        return output_str

    truncated_lines = lines[:max_lines]
    return '\n'.join(truncated_lines) + "\n... (use ClarificationIntent to see full output)"


def format_step_xml(step, step_index: int, show_full_output: bool = False) -> str:
    """Format a single step as XML with optional output truncation."""
    status = step.status

    xml_lines = [f'<task_{step_index} status="{status}">']

    if len(step.intents) > 0:
        xml_lines.append("Intents:")
        for intent in step.intents:
            intent_status = f"[{intent.status}]" if intent.status != "completed" else ""

            xml_lines.append(f"  - {intent_status} {intent.type}")

            xml_lines.append(f"    Reasoning: {intent.reasoning}")
            xml_lines.append(f"    Prev step analysis: {intent.previous_step_analysis}")
            xml_lines.append(f"    Memory: {intent.memory}")
            xml_lines.append(f"    Next task: {intent.next_task}")


            # Show args compactly
            # if intent.args and hasattr(intent.args, 'model_dump'):
            #     args_dict = intent.args.model_dump()
            #     # Filter out None/empty values for cleaner display
            #     args_dict = {k: v for k, v in args_dict.items() if v is not None and v != ""}
            #     if args_dict:
            xml_lines.append(f"    intent_args: {truncate(intent.args)}")

            # Show output (truncated or full)
            if intent.output is not None:
                if show_full_output:
                    output_str = str(intent.output) if not isinstance(intent.output, BaseModel) else intent.output.model_dump_json(indent=2)

                else:
                    output_str = truncate(intent.output)

                # Indent output lines
                output_lines = output_str.split('\n')

                for line in output_lines:
                    xml_lines.append(f"    {line}")

            # Show error if present
            if intent.error_message:
                xml_lines.append(f"    Error: {intent.error_message}")

    else:
        xml_lines.append("No intents executed")

    xml_lines.append(f'</task_{step_index}>')

    return '\n'.join(xml_lines)


def format_history_xml(agent) -> str:
    """
    Format agent history as XML with compression.
    - If ≤20 steps: show all (truncated outputs except most recent)
    - If >20 steps: first 5 + collapsed indicator + last 10
    """
    if len(agent.steps) == 0:
        return "No steps completed yet."

    total_steps = len(agent.steps)
    xml_parts = []

    if total_steps <= 20:
        # Show all steps
        for i, step in enumerate(agent.steps, start=1):
            is_most_recent = (i == total_steps)
            xml_parts.append(format_step_xml(step, i, show_full_output=False))
    else:
        # Compression: first 5 + last 10
        # First 5
        for i in range(5):
            xml_parts.append(format_step_xml(agent.steps[i], i + 1, show_full_output=False))

        # Collapsed indicator
        collapsed_count = total_steps - 15
        xml_parts.append(f'<task_collapsed>Steps 6-{5 + collapsed_count} hidden (use ClarificationIntent to view)</task_collapsed>')

        # Last 10
        for i in range(total_steps - 10, total_steps):
            step_index = i + 1
            is_most_recent = (step_index == total_steps)
            xml_parts.append(format_step_xml(agent.steps[i], step_index, show_full_output=is_most_recent))

    return '\n\n'.join(xml_parts)


def get_recent_errors(agent, look_back: int = 3) -> str:
    """Extract failed intents from recent steps for error context."""
    if len(agent.steps) == 0:
        return ""

    recent_steps = agent.steps[-look_back:]
    errors = []

    for i, step in enumerate(recent_steps):
        step_index = len(agent.steps) - look_back + i + 1
        for intent in step.intents:
            if intent.status == "failed" and intent.error_message:
                errors.append(f"Step {step_index} - {intent.type}: {intent.error_message}")

    if not errors:
        return ""

    return "\n".join(errors)


def build_dynamic_system_prompt(agent, tools: list[type[BaseModel]], user_prompt: str) -> str:
    """Build complete dynamic system prompt with current agent state."""

    # Format history
    history_xml = format_history_xml(agent)

    # Get recent errors
    recent_errors = get_recent_errors(agent)
    recent_errors_section = ""
    if recent_errors:
        recent_errors_section = f"""
<recent_errors>
{recent_errors}

Learn from these errors and adjust your approach accordingly. Do not repeat the same mistakes.
</recent_errors>
"""

    # Format tool descriptions (minimal)
    tool_descriptions = []

    for tool in tools:
        # Get input schema fields
        # params = []
        #
        # for field_name, model_field in tool.model_fields.items():
        #     field_type = model_field.annotation.__name__ if model_field.annotation else str(model_field.annotation)
        #     params.append(f"{field_name}: {field_type}")
        #
        # params_str = ", ".join(params)

        tool_descriptions.append(f"- **{tool.__name__}**: {tool.__doc__}")

    tools_section = "\n".join(tool_descriptions)

    # Build complete prompt
    prompt = f"""<role>
Autonomous agent for NYC taxi data analysis. Complete assigned tasks by performing actions using available intents.

All actions recorded as structured intents for tracking and debugging.
</role>

<history>
{history_xml}
</history>
{recent_errors_section}

<goal>
{user_prompt}
</goal>

<intents>
Check <core_principles> and <history> before choosing intents.

{tools_section}
</intents>

<core_principles>
**Decision Making**:
- Analyze <history> and <goal> before acting
- Explicitly judge success/failure from outputs, not assumptions
- NEVER repeat failed intents without changing approach
- Learn from <recent_errors> and adjust strategy

**Best Practices**:
- Explore data systematically (list files, understand schema, validate assumptions)
- Document findings incrementally (create intermediate files)
- Always validate SQL before executing complex queries
- Use DuckDB documentation when uncertain about functions/features
- Created SQL tables persist across queries - leverage this
- Use ClarificationIntent to see previous outputs when needed

**File Management**:
- Write files that will be accessible later for analysis
- Use descriptive filenames
- Reference previous work when making recommendations

**Output Requirements**:
- Return ONLY JSON array of intents (no explanatory text)
- Keep reasoning concise, use the `reasoning` field effectively
- Make sure to include `previous_step_analysis` for context
- Maintain relevant `memory` for continuity, this is KEY for you to know what you've done without re-reading full history
- Use the `next_task` field to clearly define subsequent steps
- Batch multiple intents when beneficial (parallelize independent tasks, or chain dependent ones), this improves efficiency!
</core_principles>

<output_format>
Return JSON array of intents. No text outside JSON.

The valid format for an intent is as following:

```
{{
    "type": "<IntentSchema>_Intent",
    // Note that it's called "intent_args"
    "intent_args": {{
        // Arguments specific to the intent schema, e.g. for ExecuteSQLSchema:
        "sql": "<your SQL query here>"
    }},
    "reasoning": "<brief reasoning for choosing this intent>",
    "previous_step_analysis": "<analysis of previous step outputs relevant to this intent>",
    "memory": "<(optional) relevant memory to retain for future steps>",
    "next_task": "<(optional) clear definition of the next task to perform>"
}}
```

So you should specially focus on choosing the correct intent schema and providing the correct arguments in the `intent_args` field!

Example:
```
[
  {{ "type": "ListFilesSchema_Intent", "intent_args": {{ "filter": "" }}, "reasoning": "Start by listing all available files to understand the dataset.", "previous_step_analysis": "No previous steps.", "memory": "", "next_task": "Identify relevant files for taxi trip data." }},
  {{ "type": "ExecuteSQLSchema_Intent", "intent_args": {{ "sql": "SELECT COUNT(*) FROM trips" }}, "reasoning": "Count total number of trips to get an overview of the dataset.", "previous_step_analysis": "Listed files and identified 'trips.parquet' as the main data file.", "memory": "trips.parquet contains NYC taxi trip records.", "next_task": "Analyze trip counts by day." }}
]
```
</output_format>
"""

    return prompt

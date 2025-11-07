from typing import Any
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
        xml_lines.append(f"<intents count='{len(step.intents)}'>")

        for i_ix, intent in enumerate(step.intents):
            intent_status = f"[{intent.status}]" if intent.status != "completed" else ""

            xml_lines.append(f"<intent_{i_ix + 1}>")
            xml_lines.append(f"{intent_status} {intent.type}")

            xml_lines.append(f"Reasoning: {intent.reasoning}")
            xml_lines.append(f"Prev step analysis: {intent.previous_step_analysis}")

            xml_lines.append(f"Memory: {intent.memory}")
            xml_lines.append(f"Next task: {intent.next_task}")

            xml_lines.append(f"<intent_args>\n{truncate(intent.args)}\n</intent_args>")

            # Show output (truncated or full)
            if intent.output is not None:
                if show_full_output:
                    output_str = str(intent.output) if not isinstance(intent.output, BaseModel) else intent.output.model_dump_json(indent=2)

                else:
                    output_str = truncate(intent.output)

                # Indent output lines
                output_lines = output_str.split('\n')

                xml_lines.append("<output>")

                for line in output_lines:
                    xml_lines.append(line)

                if len(output_lines) == 0:
                    xml_lines.append("<empty output>")

                xml_lines.append("</output>")

            # Show error if present
            if intent.error_message:
                xml_lines.append(f"Error: {intent.error_message}")

            xml_lines.append(f'</intent_{i_ix + 1}>')

        xml_lines.append("</intents>")

    else:
        xml_lines.append("No intents executed in this step.")

    xml_lines.append(f'</task_{step_index}>')

    return '\n'.join(xml_lines)


def format_history_xml(agent, trucate_after: int = 20, keep_start: int = 5, keep_end: int = 10) -> str:
    """
    Format agent history as XML with compression.
    """
    if len(agent.steps) == 0:
        return "No steps completed yet."

    total_steps = len(agent.steps)
    xml_parts = []

    if total_steps <= trucate_after:
        # Show all steps
        for i, step in enumerate(agent.steps, start=1):
            is_most_recent = (i == total_steps)
            xml_parts.append(format_step_xml(step, i, show_full_output=False))

    else:
        for i in range(keep_start):
            xml_parts.append(format_step_xml(agent.steps[i], i + 1, show_full_output=False))

        # Collapsed indicator
        collapsed_count = total_steps - (keep_start + keep_end)

        xml_parts.append(f'<task_collapsed>Steps {keep_start + 1} to {total_steps - keep_end} collapsed ({collapsed_count} steps)</task_collapsed>')

        # Last 10
        for i in range(total_steps - keep_end, total_steps):
            step_index = i + 1
            is_most_recent = (step_index == total_steps)
            xml_parts.append(format_step_xml(agent.steps[i], step_index, show_full_output=is_most_recent))

    return '\n\n'.join(xml_parts)


def build_dynamic_system_prompt(agent, tools: list[type[BaseModel]], user_prompt: str) -> str:
    """Build complete dynamic system prompt with current agent state."""
    # Format history
    history_xml = format_history_xml(
        agent,
        trucate_after=15,
        keep_start=5,
        keep_end=3
    )

    tools_list_str = ""

    for t in tools:
        tools_list_str += f"<{t.__name__}>\n{t.__doc__ or 'No description available.'}\n</{t.__name__}>\n"

    # Build complete prompt
    prompt = f"""<role>
Autonomous agent for NYC taxi data analysis. Complete assigned tasks by performing actions using available intents.

All actions recorded as structured intents for tracking and debugging.
</role>

<history>
{history_xml}
</history>

<goal>
{user_prompt}
</goal>

<available_intents>
Use the following intents to perform actions:

{tools_list_str}
</available_intents>

<core_principles>
**Decision Making**:
- Analyze <history> and <goal> before acting (choose intents based on evidence)
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

# Everybody talks about context, nobody is helping...

Last week I was procastinating in LinkedIn, and I stumbled upon this post:

<post>

to which I answered:

<post>

So... here's the blog that I promised :)

# Some background

I've been following the AI space really closely for the last year or so, and one thing that seems to be trending in the last months is how important is context engineering. In fact, I would say that more and more people start caring "less" about the context window (when it's more than ~0.5M tokens more or less) as it's clear that one-shotting is not the way to go anymore. Instead, a lot of conversations, and even companies, are focused on finding the best way to "engineer" the context of the models to achieve the best results in complex tasks.

At the same time, AI agents seem to be the way to go now. Eventhough MCPs got normalized, everybody is trying to find ways to build agentic systems either as a startup or as a feature in their product. You can see the latest YC batches, or the push for tools like Claude Code, Codex, Cursor Agents, etc. (in the realm of programming).

If you combine both these trends in the same canvas, what you can see is that they are highly interconnected. In fact, some of the "agents are just LLM calls in a for loop" promoters do not really apply anymore. That type of agent is "useless".

Hence, I decided to spend some time to try to think around this crosswalk, and specifically how can a random techie build an AI agent in 2026. Yes, 2026, because 2025 agent are already outdated :D

## What is an agent (in this _context_)?

Before going into my thoughts, let's clarify what an agent is for me:

> An agent is fully / human supervised process that uses LLMs and a set of heterogeneous tools to achieve a specific non-trivial task. 

Where non-trivial means that the task can not be one-shotted, neither solved ina few rounds. But rather require phases like researching, planning, analyzing and providing a clear deliverable.

## How to build an agent in 2026

I'll be brief here.

So there are multiple ways to build an agent now, probably the most common one due to it's immense distribution is LnagChain. LangChain offers multiple abstractions to build agents, you can:

1. Use the raw LLM models and build a for loop;
2. Use abstractions like `create_agent` to build simple agents;
3. Use `create_deep_agent` to build a Claude Code like agent with filesystem and tasks.

If you do not want to use LangChain, then you can go to other frameworks like the OpenAI agent framework, and the Google ADK, but probably there's like +1k frameworks out there that offer similar functionalities.

Finally, there's the good old way: building it yourself.

I won't go into other tools like n8n, or similar in which you do not controll the 100% of the logic, in particular the code.

On how to interact with LLMs, I leave that as an exercise to the reader. And if I missed some other essentially different way to build agents, please reach out!

## What about context?

If you look at all the methods to build an agent, and search on how to actually build one, everything is highly focused on how to orchestrate the code to be able to have an agentic loop. They offer more or less clear abstractions, or more utilities. In essence: they focus on DevEx and minimizing lines of code.

This is essentially wrong. Hear me out.

The real challenge (as usual) is not generating code. Having a cleaner or more messier codebase should not be your main concern in regards to AI now. The world is moving so fast that spending time to have the cleaner DevEx is not worth it, when what matters is the outcome you can get. And I say this because:

1. Writing code is not a bottleneck (it never was, but now even less);
2. Deploying your code is almost trivial (each day there's a new "use deploy" that one-clicks your code to the cloud);
3. What your users interact with is the output of your agent, not the code.

Note: If you are an OSS mantainer or someone that ships pure software, then yes, code quality matters. But for 99% of the use cases, it does not.

If we assume that 1, 2 and 3 are true, then what matters is how you can leverage the frameworks and LLMs available to get the biggest impact (a.k.a. the "wow" effect)? By taking control. And controlling this tuple can only be done by mastering context engineering. Why?

1. Frameworks are just shorcuts, so it's a matter of how to get there faster;
2. LLMs are out of your control, so you need to find the best one for your use case, and squeeze the most out of it.

Hence, the real challenge is to optimize the connection between the framework and the LLM: context.

## Different approaches into context engineering

To illustrate three basic examples using the latest tools avilable I decided to build three variants of agents:

1. "raw": A simple `create_agent` with an append-only message history;
2. "summarization": A `create_agent` that uses an auto-summary middleware to compress the message history. I used 12k context with 20 messages to keep (as per the guide above);
3. "intent": A custom agent that controls the context deterministically.

You can see all the code here: ...

The tools I gave the agent are the following:

- `list_files`: List files in a `data` directory with ~1GB of NYC taxis data from 2025 in parquet files.
- `write_file`: Be able to write arbitrary files in the `data/content` directory.
- `read_file`: Be able to read files from the `data` directory.
- `update_file`: Be able to update files in the `data` directory (similar to how Claude Code does it).
- `validate_sql`: Validates SQL (DuckDB dialect) queries for correctness.
- `execute_sql`: Executes SQL (DuckDB dialect) queries in a temporal DuckDB instance, persisted during the agent run.
- `read_docs`: Access to the DuckDB documentation in Mardkown format, starting from the [sitemap](https://duckdb.org/sitemap).

And the task is the following:

<code>
Using the NYC taxi trip dataset, analyze the market and create a fleet deployment recommendation analysis.

**Required Deliverables:**

You will need to create the following files with the specified content:

1. **`data_profile.txt`**: Document the dataset (row count, date range, key columns, any data quality issues)

2. **`zone_rankings.csv`**: Top 10 zones by profitability with columns:
   - zone_name
   - total_trips
   - total_revenue
   - avg_fare
   - avg_trip_duration_minutes

3. **`temporal_analysis.csv`**: Hourly performance (0-23) with columns:
   - hour
   - avg_trips_per_day
   - avg_fare
   - revenue_per_hour

4. **`route_matrix.csv`**: Top 15 pickup-dropoff pairs with columns:
   - pickup_zone
   - dropoff_zone  
   - trip_count
   - total_revenue
   - avg_fare
   - avg_distance_miles

5. **`efficiency_metrics.json`**: Key performance indicators:
```json
   {
     "best_revenue_zone": "Zone <ID>",
     "best_revenue_hour": 18,             // Hour of day (0-23)
     "avg_revenue_per_trip": 15.50,       // For all the applicable filtered trips
     "optimal_distance_bracket": "2-5mi", // E.g., "0-1mi", "1-2mi", "2-5mi", "5-10mi", "10+mi" to maximize revenue
     "trips_below_min_fare": 1234,        // I.e. trips with fare <= $2.50
     "trips_above_max_distance": 56       // I.e. trips > 100 miles
   }
```

**Constraints for the efficiency analysis:**
- Consider only trips with fare > $2.50 (minimum viable)
- Filter out trips > 100 miles (data errors)

Document your exploration process. I'll validate the CSVs and JSON can be parsed and matched against expected results.
</code>

You can see that the task is non-trivial, and requires multiple steps to be solved. And it forces the agent to perform multiple non-trivial queries using DuckDB, persisting files and finally generating the deliverable: the `efficiency_metrics.json`.

In the evaluation, I ran multiple models with the same iteration limit (100) and exactly the same tools and files available. And I stored in the `output` directory the results of each run for the three agents.

Later on I compared and analyzed the results in various dimensions, specially focusing on:

- Success (either it finished the task or not)
- Accuracy (when successful, how accurate were the results)
- Context usage (total and per step)
- Latencies
- Cost

The models choosen were: `anthropic-claude-sonnet-4.5`, `openai-gpt-4.1-mini`, `google-gemini-2.5-pro`, `openai-gpt-4.1`. I chose those because they were the ones that were the fairest for all three agents. Some of the other ones I tried were:

- GPT-5. Worked but all the agents decided to stop at the end and confirm with the user to proceed.
- Grok (4 and 4-fast). Struggled with tool calling, kept trying to use text output (which makes it harder for the simple agents, so not considered).
- Gemini flash (2 and 2.5). Went super fast but struggled to comback from errors. Consistently ended in a loop and consumed all iterations.
- I did not try Opus due to pricing.

### Results

#### Success rates

The most important thing to check first is success rates. I.e., did the agent finish the task or not? For that the "intent" agent scored a 100% rate in all models and all runs. The second best was the raw with only flakiness in GPT-4.1-mini, and the last one with pretty bad results was the summarization one.

<pic>

#### Accuracy

The accuracy was not the best in general, probably due to the models used. However you can see that the intent one scored consistently higher across models than the other two, which were pretty close to each other, in fact they followed similar patterns, being the summarization one slightly worse.

<pic>

#### Context usage

Before checking the result in terms of context, I want to note how much steps each agent needed to finish the task, which surprised me:

<pic>

Where you can see that the intent one is consistent even accross models and much less than the other two (<25 steps).

Now in terms of context usage, I analyzed the token usage, both for input and output, and the results were the following:

<pic>

Where you can see a clear difference in the raw one, being the highest, and the summarization and intent being pretty close.

#### Latencies

The intent one was the slower one. I used OpenRouter and generally the latencies might not be super consitent. In general all were able to finish in less than 4 minutes.

<pic>


#### Cost

Finally, I will mention cost, in which obviously the raw one won, and then the summarization one was pretty close to the intent or even cheaper. This is not surprising due to the nature of summarization being a plateau in terms of context limits. Check the section below for more details on this.

<pic>

#### Full report

You can see the full report here: ...

## How the results relate to context engineering

So... what can we learn from the results above? It might seem confusing, as there's no clear winner in all categories. But it is: the intent one is the best one. Why? The goal of the user was to get a specific deliverable, and the only agent that managed to (100% of the times) deliver it was the intent one.

Let's breakdown each metric, focusing on latency and cost first.

In terms of latencies, I saw a difference in the unit of ~60s, which for an agentic flow is nothing. These flows are meant to run in the background, or even when running interactively the users are used to +10m wait times for things like the ChatGPT or Claude deep researchs anyways. It was never about sub-second latencies anyway.

On costs, the difference is really between the summarization and the intent one, as the raw one was the more expensive one. Now taking into account the inconsistent success of the summarization anyone would want to pay a few dollars more for a guaranteed success.

Ok, now what about accuracy? To be honest, and this is purely from my experience, accuracy has more to do with the model than anything you might be able to control. You can see that the more expensive models are the best, that's it.

Now that we cleared these out, let's talk about context!!

### Raw

The raw agent is the simplest one. It just appends context on each turn, and the agent is able to see the full history of what happened. This is good for small conversations, but as the number of steps increase, the context becomes noisy, and the model struggles to find the relevant information (needle in a haystack problem). This is specially true when the model has to deal with errors, or complex reasoning.

In this particular user task, I made it so that adding to the stack is expensive, as you would be calling tools like `write_file` or `execute_sql` that would generate a lot of context. Hence, the model would struggle to find the relevant information in the context, and would often forget what it was doing, or make mistakes.

So no surprise that the raw agent ate the most context of all.

### Summarization

This one is pretty similar to the raw agent, but after hitting a threshold (12k tokens in this case), it would summarize the context to compress it. This is good in theory, as it would reduce the noise in the context, and help the model focus on the relevant information. Nevertheless, in an analytical task like this one, where a number going a unit up or down matters, summarization can be harmful, as it might lose important details.

In particular, I had to adapt the default summarization strategy to force the summarization model keep the original user task, as I saw that by default it would completely hallucinate and forget what the user wanted to achieve. This may be improved by using a better summarization model, but it would incurr in added costs and no real guarantees.

On the good side, the context is capped, so you can "fine-tine" the summarization threshold to optimize performance for the type of tasks you want to solve, but my guess is that it would require a lot of testing, tuning and dependance on the type of user task (e.g. if the initial task automatically exceeds the threshold, then it would be useless).

### Intent

Finally the intent approach. This is a completely custom LLM history approach. The idea is pretty simple: distill what the agent essential goal is, and write down a "prompt template" that you overwrite on each step with your progress (see the code here: ...).

This, obviously, is more tedious and has a default context bump, as the template might be larger than a simple system prompt in the first two agents. Also, it will grow with time, as you add more and more steps.

The good thing, as you can see is that it requires generally less steps due to the determinisitic compactificataion (R), and is scales more linearly than the raw approach.

<pic_token_step_rel>

## Conclusion

The conclusion is pretty simple: context engineering (control) matters. A lot. The more you control the context, the better the final results you will get. 

In particular, I wanted to summarize the three strategies analyzed in the following charts.

<chart_raw>

As simple as that, the more to dump into it the less you will get out of it. That's why Claude Code has auto-compactification.

<chart_summarization>

In this case, it's clear. The kids game of the broken telephone. The more you summarize, the more you lose. Maybe after the 4th summary you do not even know what the original task is, so probably 42, right?

<chart_intent>

And this is the proposed intent approach. Simple, but effective. The more you control the context, the better the results. But, as usual, it will grow, so it also has it's limits, yet more controllable and higher ceiling than the other two.

### Ok... what should I do then?

As usual, there's no "silver bullet". However, I would recommend the following:

<comparison>

1. If you have a simple agent, just go for the raw approach. It will work fine. If you do not need a lot of tools, and just want to iterate a few times to get a result, it will be more than fine.
2. If you are building a more complex agent, then I would recommend going for the intent approach. It will require more work, but the results will be worth it.
3. If you are building an extremely complex flow, then you should probably consider splitting, or having a Human-in-the-loop (HITL). 

<human_leverage>

## Next steps

If you read this to this point, I love you. If you disagree with me, I love you even more and please reach out to me to discuss!

Personally, I find this context engineering topic super interesting and as something that evolves so fast, maybe this post will be useless in a month, who knows.

But, here's a few things that I want to explore next:

- Figure out if there are context driven libraries. To start, found this in the LangChain docs: https://docs.langchain.com/oss/python/concepts/context#dynamic-runtime-context
- Check out how context and agent getting better coding come into play together to make complex tool call chains easier with code: https://www.anthropic.com/engineering/code-execution-with-mcp

## References

Here's a set of references I found extremely useful in the last months, and during the writing of this blog:

- Middleware article: https://codecut.ai/langchain-1-0-middleware-production-agents/
- BAML: https://github.com/BoundaryML/baml
- 12 factor agents: https://github.com/humanlayer/12-factor-agents
- Advanced Context Engineering: https://github.com/humanlayer/advanced-context-engineering-for-coding-agents
- Great HumanLayer video to YC: https://www.youtube.com/watch?v=8kMaTybvDUw
- Manus about context: https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus
- Claude about context: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Needle in a haystack (concept), some references:
    - https://blog.langchain.com/multi-needle-in-a-haystack/
    - https://cloud.google.com/blog/products/ai-machine-learning/the-needle-in-the-haystack-test-and-how-gemini-pro-solves-it
    - https://arxiv.org/abs/2407.01437

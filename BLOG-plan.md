# A (deep) dive into Context Engineering

1. Motivation
    1.1. LinkedIn post on summarization middleware
    1.2. Experience with context hell and reply

2. Let's define an agent

3. What options you have to code agents?
    - LangChain - multiple alternatives, from manual, simple agents to deep agent
    - OpenAI / Google SDKs - basic agents
    - Manual
    - Other libraries - please let me know if there's a good one

4. How important is context

5. What I did (super high-level)

6. Analysis of results

7. Conclusion

8. Next steps

9. References

## The ultimate goal

To understand the consequences of uncontrolled context in agentic flows. Specially how intentful (determinisitic) compactification can affect the performance of agents in long running sessions with a lot of tools.

1. As deterministic as possible
2. 100% control over context
3. Ensure completion

## Next steps

- Figure out context driven libraries VS process driven libraries
    - There's https://docs.langchain.com/oss/python/concepts/context#dynamic-runtime-context
- https://www.anthropic.com/engineering/code-execution-with-mcp

## Notes

Tried

- gpt-5, worked but all the agents decided to stop at the end and confirm with the user to proceed?
- grok (4 and 4-fast), struggled with tool calling, kept trying to use text output (which makes it harder for the simple agents, so not considered)
- gemini flash (2 and 2.5), went super fast but struggled to comback from errors, ending up in a loop and exceeding the max steps

did not try opus or other reasoning / expensive models for pricing reasons

## References

- Middleware article: https://codecut.ai/langchain-1-0-middleware-production-agents/
- BAML: https://github.com/BoundaryML/baml
- 12 factor agents: https://github.com/humanlayer/12-factor-agents
- Advanced Ctx Engineering: https://github.com/humanlayer/advanced-context-engineering-for-coding-agents
- HumanLayer video: https://www.youtube.com/watch?v=8kMaTybvDUw
- Manus Context: https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus
- Calude Context: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Needle in a haystack (concept)
    - https://blog.langchain.com/multi-needle-in-a-haystack/
    - https://cloud.google.com/blog/products/ai-machine-learning/the-needle-in-the-haystack-test-and-how-gemini-pro-solves-it
    - https://arxiv.org/abs/2407.01437

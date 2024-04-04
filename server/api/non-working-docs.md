[OpenAI Assistant Docs](https://python.langchain.com/docs/modules/agents/agent_types/openai_assistants)

```python
interpreter_assistant = OpenAIAssistantRunnable.create_assistant(
    name="langchain assistant",
    instructions="You are a personal math tutor. Write and run code to answer math questions.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-1106-preview",
)
output = interpreter_assistant.invoke({"content": "What's 10 - 4 raised to the 2.7"})
output
```

Error:
```python
...
assistant = client.beta.assistants.create(
    211     name=name,
    212     instructions=instructions,
--> 213     tools=[convert_to_openai_tool(tool) for tool in tools],  # type: ignore
    214     model=model,
...
ValueError: Unsupported function

{'type': 'code_interpreter'}

Functions must be passed in as Dict, pydantic.BaseModel, or Callable.
If they're a dict they must either be in OpenAI function format or
valid JSON schema with top-level 'title' and 'description' keys.
```

Should be closed in [PR #19081](https://github.com/langchain-ai/langchain/pull/19081) when it is merged to master
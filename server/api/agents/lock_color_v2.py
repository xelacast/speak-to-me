from langchain.prompts import MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain_openai import ChatOpenAI
from langchain.agents import tool
from langchain.agents import AgentExecutor


llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# ==== Custom Function for appending messages to chat history === #

def inovoke_and_append(input: str, chat_history: list):
    result = agent_executor.invoke({"input": input, "chat_history": chat_history})
    chat_history.extend(
        [
            HumanMessage(content=input),
            AIMessage(content=result["output"]),
        ]
    )
    return result

# ==== Custom tooling === #
@tool
def get_word_length(word: str) -> int:
    """Returns the length of the input word."""
    return len(word)

tools = [get_word_length]

llm_with_tools = llm.bind_tools(tools)


# ===== Chat History and Prompt ===== #
# https://python.langchain.com/docs/expression_language/how_to/message_history check this for more in depth explanation
chat_history = []
memory_key = "chat_history"

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are very powerful assistant, but bad at calculating lengths of words.",
    ),
    MessagesPlaceholder(variable_name=memory_key),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])


# ===== Agent and chain ===== #
agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
        "chat_history": lambda x: x["chat_history"],
    }
    | prompt
    | llm_with_tools
    | OpenAIToolsAgentOutputParser()
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
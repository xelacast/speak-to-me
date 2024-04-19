from langchain_openai import ChatOpenAI
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ChatMessageHistory

from langchain.pydantic_v1 import BaseModel, Field

from typing import Optional


#### OUTPUT SCHEMA ####
class LockState(BaseModel):
    color: Optional[str] = Field(description="FORMAT TEXT COLORS TO HEX. First color found. If no color is found then return none. Format the color to hex format before returning.")
    lock_type: Optional[str] = Field(description="The type of lock to be updated. The VALUES to choose from: ['open', 'closed', 'none', 'half-opened']")

system_prompt = """
You are an expert extraction algorithm.
Only extract relevant information from the text.
If you do not know the value of an attribute asked to extract,
return null for the attribute's value.

Parse the text and find a color and lock type if present.

Turn all colors to hex format.

- Values for the lock_type can ONLY be 'open', 'closed', 'none', 'half-opened'

Turn output into JSON with keys of 'color' and 'lock_type'


TAKE YOUR TIME TO THINK
"""

# 1 init model
model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# 2 create prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            system_prompt
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ]
)
# 2 create chat History
chat_history = ChatMessageHistory()
chat_model_with_tools = model.with_structured_output(LockState)
chat_chain = prompt | model

chat_chain_with_history = RunnableWithMessageHistory(
    chat_chain,
    lambda session_id: chat_history,
    input_messages_key="input",
    history_messages_key="chat_history"
)
#!/usr/bin/env python

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langserve import add_routes
import uvicorn
from dotenv import load_dotenv, find_dotenv
from langchain.schema.runnable import RunnableLambda

# from api.chat import ChatHistory, chat_model, chat_message_bot, ChatHistoryMessage, FileProcessingRequest, procFBess_file

from langchain.tools import StructuredTool, tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
import json
from langchain.chains.structured_output.base import create_structured_output_runnable
import requests
from langchain.tools.render import render_text_description_and_args, render_text_description

from api.agents.lock_color_v2 import agent
from api.agents.chat_with_history import chat_chain_with_history




load_dotenv(find_dotenv())

# ===== Custom Tool ===== #
@tool
def sendColor(color: str, lock_type: str, message: str) -> str:
    """Sends a post request to an API Endpoint to update the color of the emoji"""
    print("BIG COLOR HERE:", color)
    if (message == 'failure'):
        color = '#000000'
    requests.post("http://localhost:3000/api/lockcolor", json={"color": color})

    return json.dumps({"color": color, "message": message, "lock_type": lock_type})

class RecordColor(BaseModel):
    """Record some identity of the color"""
    color: str = Field(description="The color found in the text in hex value format")
    message: str= Field(description="The message to be sent back to the user. Either 'success' or 'failure'")
    lock_type: str = Field(description="The type of lock to be updated. Can be either 'open' or 'closed' or 'none' or 'half-opened'")

color = StructuredTool.from_function(
    func=sendColor,
    name="sendColor",
    description="useful for when you need to send the input color to an api",
    args_schema=RecordColor,
    return_direct=True
)

# ==== App initialization ==== #
app = FastAPI(
    title="Langchain server",
    version="0.1.0",
    description="A simple server for OpenAI api",
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=True, expose_headers=["*"])

model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, verbose=True).bind_tools([color])



# prompt = ChatPromptTemplate.from_template("""You are a helpful color assistant. You have a kein eye for spotting colors in text. You can help me find the color in a text decorated in backticks. If there is no color, return 'black'. Colors are valid in hex, rgba, or color name format. DO NOT return any other information besides the color. Send this information to the Custom Tool color. Your response should be a 'success' if the the tool returns a color or 'failure' if the getColor tool returns black.

# v3 = """parse the text and find the color. your output will be in JSON format with the key color. Example. Incoming text is "I want a blue pair of jeans", output is {{"color":"blue"}}. If no color is found then the value will be "black". If there is MORE than one color found only use the first color. Send the value of the color to the Custom Tool. {input}"""

# `{text}`""") - Send the value of the color to the Custom Tool. - Send back content of a JSON object with key value pair of color and the color value. Example {{"color": "#444000"}}

template = """
parse the text and find a color if present

Example. Incoming text is "I want a blue pair of jeans", output is "blue".

- If no color is found then the value will be "black".
- If there is MORE than one color found only use the first color.
- Convert the color to hex format before sending it to the Custom Tool.
- Send only the first value of the color(s) to the Custom Tool.

{input}"""

prompt = ChatPromptTemplate.from_template("""
parse the text and find a color if present

{input}""")

parser = JsonOutputParser()

structured_llm = create_structured_output_runnable(
    RecordColor,
    model,
    mode="openai-tools",
    enforce_function_usage=True,
    return_single=True,
    )


add_routes(
    app,
    structured_llm,
    path="/colors"
)

# ==== Color and Lock ==== #
class LockColor(BaseModel):
    color: str = Field(description="FORMAT TEXT COLORS TO HEX FORMAT. First color found. If no color is found then 'black' is the color. Format the color to hex format before returning.")
    lock_type: str = Field(description="The type of lock to be updated. The VALUES to choose from: ['open', 'closed', 'none', 'half-opened']")
    message: str= Field(description="The message to be sent back to the user. Either 'success' or 'failure'")

@tool
def formatResponse(color: str, lock_type: str, message: str):
    """Send JSON object back to the client with the color and message and lock type."""
    return json.dumps({"color": color, "message": message, "lock_type": lock_type})

req = StructuredTool.from_function(
    func=formatResponse,
    name="FormatResponse",
    description="Format JSON response for client",
    args_schema=LockColor,
    return_direct=True
)


# ==== Lock Color Endpoint ==== #

lockColor = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, verbose=True)

system_prompt = f"""
parse the text and find a color and lock type if present

Example: Incoming text is "I want a blue pair of jeans and a lock thats opened". Lock type is 'open' color is 'blue'.
Example: I want a shut lock that is #8a251e. lock_type is 'closed' color is '#8a251e'.

- If no color is found then the value will be "black".
- If there is MORE than one color found only use the first color.
- Convert the color to hex format before sending it to the Custom Tool.
- Send only the first value of the color(s) to the Custom Tool.

- THE ONLY values the lock_type can be are: 'open', 'closed', 'none', 'half-opened'. DO NOT RETURN ANY OTHER VALUES.
- If NO lock type is found then the value will be "open".
- If there is MORE than one lock type found only use the first lock type.

- Do not decide the value of the lock until you have read all instructions and the text.
- FORMAT THE COLORS TO HEX FORMAT

TAKE YOUR TIME TO THINK

{input}
"""

prompt = ChatPromptTemplate.from_messages(
    [("system", system_prompt), ("user", "{input}")]
)


# This is overriding the prompt rules with the arg schema
lock_and_color_llm = create_structured_output_runnable(
    LockColor,
    model,
    mode="openai-tools",
    enforce_function_usage=True,
    return_single=True,
    )

json_chain = prompt | lock_and_color_llm

add_routes(
    app,
    json_chain,
    path="/lockcolor"
)

# Chat with chat history
add_routes(
    app,
    agent,
    path="/lockcolor-v2"
)

add_routes(
    app,
    chat_chain_with_history,
    path="/chatbot"
)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
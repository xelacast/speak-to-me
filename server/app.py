#!/usr/bin/env python

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langserve import add_routes
import uvicorn
from dotenv import load_dotenv
from langchain.schema.runnable import RunnableLambda


from api.chat import ChatHistory, chat_model, chat_message_bot, ChatHistoryMessage, FileProcessingRequest, process_file

load_dotenv()


app = FastAPI(
    title="Langchain server",
    version="0.1.0",
    description="A simple server for OpenAI api",
)


app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=True, expose_headers=["*"])

add_routes(
    app,
    ChatOpenAI(),
    path="/openai"
)

model = ChatOpenAI()
prompt = ChatPromptTemplate.from_template("write me fantasy short stories about {topic}. Create max length to 75 words.")
prompt1 = ChatPromptTemplate.from_template("write a poem about {topic}. Make it 5 lines long maximum.")


add_routes(
    app,
    prompt | model,
    path="/fantasy-stories"
)

add_routes(
    app,
    prompt1 | model,
    path="/poem"
)

add_routes(
    app,
    chat_model.with_types(input_type=ChatHistory),
    config_keys=["configurable"],
    path="/chat",
)

add_routes(
    app,
    RunnableLambda(chat_message_bot).with_types(input_type=ChatHistoryMessage),
    config_keys=["configurable"],
    path="/chat_message",
)

add_routes(
    app,
    RunnableLambda(process_file).with_types(input_type=FileProcessingRequest),
    config_keys=["configurable"],
    path="/pdf",
)



if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8006)
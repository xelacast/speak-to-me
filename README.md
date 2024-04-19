# SpeakToMe

# Description

Chat with the lovely chat to change the state and color of the lock.

### Roadmap

- [x] GPT can interpret unstructured data to alter send back specific data.
- [ ] Make chatbot have a personality and send back a conversations
- [ ] Voice to chat interactions.
- [ ] Integrate chat model into application functionality (chat to action)

# Motivation
I was bored and wanted to add a cool feature to the other application I am currently working on. Theres a few things I wanted to try and build here before I did that. I also wanted to learn Langchain and ChatGPT more in depth to potentially change my career.

# Quick Start

Clone the repository
```bash
git clone git@github.com:xelacast/speak-to-me.git
```

Requirements:
- Node.js 18+
- pnpm
- docker
- python3.11+

## Client
Follow the bash commands below to run the projects

```bash
cd web && cp .env.example .env && pnpm i && pnpm dev --turbo
```

Then travel to http://localhost:3000

## Server
Open a new bash terminal to run the commands in

```bash
cd server && cp .env.example .env && python3 -m venv .venv && source ./.venv/bin/activate && pip install -r requirements.txt
```
You must insert your environment variables NOW. The only REQUIRED variable is the OPENAI_API_KEY. The app is running off of ChatGPT so you must use an OpenAI api key.

(Optional) The app is using Langchain with Langsmith and Langserve so <b>you can create a langsmith account and api key if you want tracing</b>

Once you have the OpenAI API key placed into your .env run the following
```bash
python3 main.py
```

This will run the server on http://localhost:8000


Endpoints can be seen at http://localhost:8000/docs

# ⚙️ Usage

Travel to http://localhost:3000 after setup and talk to the chatbot. Right now it can only take in commands to change its color and to change the lock to a state of 'opened' 'closed' 'half-opened'. The GPT will inference the color and state based off the text input. If it doesn't find a color or state it will default to 'closed' and 'black'.


Travel to http://localhost:8000/lockcolor/playground to interact with the endpoint

# 🤝 Contributing

Feel free to contribute
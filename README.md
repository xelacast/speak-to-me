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
NOTE: The client side is using pnpm package manager
Run the bash client script for a quick setup. <em>This will install pnpm globally using npm</em>

```bash
start-client.sh
```

OR do it manually
```bash
cd web && cp .env.example .env && pnpm i && start-database.sh && pnpm dev --turbo
```

Then travel to http://localhost:3000

## Server

```bash
cd server && cp .env.example .env && python3 -m venv .venv && python3 install -r requirements
```
You must insert your environment variables NOW. The only REQUIRED variable is the OPENAI_API_KEY. The app is running off of ChatGPT so you must use an OpenAI api key.

(Optional) The app is using Langchain with Langsmith and Langserve so <b>you can create a langsmith account and api key if you want tracing</b>

Once you have the OpenAI API key run the following
```bash
python3 main.py
```

This will run the server on http://localhost:8000


Endpoints can be seen at http://localhost:8000/docs

# ⚙️ Usage

Travel to http://localhost:3000 after setup and talk to the chatbot. Right now it can only take in commands to change its color and to change the lock to a state of 'opened' 'closed' 'half-opened'. The GPT will inference the color and state based off the text input. If it doesn't find a color or state it will default to 'closed' and 'black'.

# 🤝 Contributing

Feel free to contribute
#!/usr/bin/env bash
# web startup

# Client
## Check if pnpm is installed
if ! command -v pnpm &> /dev/null; then
    echo "pnpm not found. Installing..."
    npm install -g pnpm
    if [ $? -eq 0 ]; then
        echo "pnpm has been installed successfully."
    else
        echo "Failed to install pnpm. Please check your network connection and try again."
        exit 1
    fi
else
    echo "pnpm is already installed."
fi

cd web && cp .env.example .env

## install and run dev env
pnpm i && start-database.sh && pnpm dev --turbo



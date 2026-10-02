#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ -d "venv" ]; then
    source venv/bin/activate
fi

if [ ! -f ".env" ]; then
    echo "No .env found. Copy .env.example to .env and set your GEMINI_API_KEY."
fi

uvicorn legalEaseAPI.main:app --reload --port 8000 &
API_PID=$!

trap "kill $API_PID" EXIT

sleep 2
streamlit run frontend/app.py

wait $API_PID

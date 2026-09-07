#!/bin/sh

set -e

if [ ! -d ".venv" ]; then
    echo "Installing Python dependencies..."
    poetry install
fi

echo "Starting FastAPI..."

exec poetry run uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload
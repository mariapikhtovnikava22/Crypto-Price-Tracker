#!/bin/bash
set -e

echo "Applying database migrations..."
alembic upgrade head

echo "Starting FastAPI application..."
exec python main.py start
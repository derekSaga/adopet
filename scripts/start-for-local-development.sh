#!/usr/bin/env bash
export PYTHONPATH=adopet

set -e

alembic upgrade head

uvicorn main:app --host 0.0.0.0 --port "$API_PORT" --log-config logging.yaml
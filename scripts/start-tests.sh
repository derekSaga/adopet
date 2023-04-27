#!/usr/bin/env bash
export PYTHONPATH=adopet/

echo $PYTHONPATH

python -m pytest --log-cli-level=DEBUG -vv --cov=adopet --junitxml=junit/test-results.xml --cov-report=xml --cov-report=html --cov-report=term --cov-append

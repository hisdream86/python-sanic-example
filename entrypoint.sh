#!/bin/bash

if ! alembic upgrade head; then
  exit 1
fi
python main.py
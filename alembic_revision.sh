#!/usr/bin/env bash
NEXT_ID=`ls alembic/versions/* | grep -E '/\d{4}_.*\.py$' | wc -l`
alembic revision --rev-id=`printf "%04d" ${NEXT_ID}` "$@"
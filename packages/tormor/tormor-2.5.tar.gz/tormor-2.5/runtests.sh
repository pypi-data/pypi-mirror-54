#!/bin/bash
set -eux
cd $(dirname 0)
bash tormor/tests/cleanup.sh
bash tormor/tests/bootstrap.sh
SCHEMA_PATH="$(pwd)/tests/Schema:$(pwd)/tests/Schema2" PYTHONPATH="$(pwd)" && pytest -v $*

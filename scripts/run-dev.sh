#!/bin/sh

# Launches development containers
# ./scripts/run-dev.sh

# You can also pass various arguments, for example:
# ./scripts/run-dev.sh -d --build

docker-compose -f docker-compose.dev.yml --profile dev up "$@"

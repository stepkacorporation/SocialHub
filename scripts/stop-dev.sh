#!/bin/sh

# Stops and removes development containers
# ./scripts/stop-dev.sh

# You can also pass various arguments, for example:
# ./scripts/stop-dev.sh -v

docker-compose -f docker-compose.dev.yml --profile dev down "$@"

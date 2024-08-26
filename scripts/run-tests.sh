#!/bin/sh

# ./scripts/run-tests.sh

# You can also pass various pytest arguments, for example:
# ./scripts/run-tests.sh -v --disable-warnings

# Launches containers for tests
docker-compose -f docker-compose.dev.yml --profile test run --rm web-test pytest "$@"

# Stop and delete containers
docker-compose -f docker-compose.dev.yml --profile test down -v

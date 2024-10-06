#!/bin/bash

# Initializing project's files.
chmod +x ./scripts/init.sh
./scripts/init.sh

# Removing pre-existing containers
docker compose -f ./docker-compose_backdev.yml down -v --remove-orphans
# Building the new containers.
docker compose -f ./docker-compose_backdev.yml up -d --remove-orphans

# Running the application.
chmod +x ./scripts/run.sh
./scripts/run.sh

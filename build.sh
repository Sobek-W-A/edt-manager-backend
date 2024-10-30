#!/bin/bash

function clean_up_stack() {
  local compose_file="$1"

  echo "[STATUS] - Cleaning up stack defined in ${compose_file}"

  # Stop and remove containers, networks, and volumes associated with the specified compose file
  docker compose -f "${compose_file}" down -v --remove-orphans
  # Remove dangling images specific to this compose file (only those not used by other containers)
  docker images -f "dangling=true" -q | xargs -r docker rmi
  # Remove any anonymous or dangling volumes specific to this stack
  docker volume prune -f
  # Cleaning the older images
  docker rm -f $(docker ps -a -q --filter "name=sobekwa")
  docker rmi -f $(docker images -q --filter "reference=sobekwa*")

  echo "[STATUS] - Stack cleaned up successfully."
}

function run_dev() {
  echo "[STATUS] - Running Development environment."

  # Clean up the development stack
  clean_up_stack ./docker-compose_backdev.yml

  # Build and start the containers with no cache
  docker compose -f ./docker-compose_backdev.yml build --no-cache
  docker compose -f ./docker-compose_backdev.yml up -d --remove-orphans --force-recreate

  # Run the application script
  chmod +x ./scripts/run.sh
  ./scripts/run.sh
}

function run_bundle() {
  echo "[STATUS] - Running Bundled environment."

  # Clean up the bundled stack
  clean_up_stack ./docker-compose.yml

  # Build and start the containers with no cache

  docker compose -f ./docker-compose.yml build --no-cache --build-arg CACHEBUST=$(date +%s)
  docker compose -f ./docker-compose.yml up -d --remove-orphans --force-recreate
}

function run_prod() {
  echo "[STATUS] - Running Production environment."

  # No stack clean-up to retain the production state
  docker compose -f ./docker-compose.yml up -d --remove-orphans
}

# Variables:
ENVIRONMENT="$1"
PROD="production"
DEV="development"
BUNDLE="bundle"

# Initializing project's files.
chmod +x ./scripts/init.sh
./scripts/init.sh

if [[ -n "$ENVIRONMENT" ]]; then
  if [[ "$ENVIRONMENT" == "$DEV" ]]; then
    run_dev
  elif [[ "$ENVIRONMENT" == "$BUNDLE" ]]; then
    run_bundle
  elif [[ "$ENVIRONMENT" == "$PROD" ]]; then
    run_prod
  fi
else
  run_dev
fi

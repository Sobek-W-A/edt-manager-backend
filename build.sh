#!/bin/bash

function run_dev() {
  echo "[STATUS] - Running Development environnnement."

  # Removing pre-existing containers
  docker compose -f ./docker-compose_backdev.yml down -v --remove-orphans
  # Building the new containers.
  docker compose -f ./docker-compose_backdev.yml up -d --remove-orphans

  # Running the application.
  chmod +x ./scripts/run.sh
  ./scripts/run.sh
}

function run_bundle() {
  echo "[STATUS] - Running Bundled environnnement."


  # Removing pre-existing containers
  docker compose -f ./docker-compose.yml down -v --remove-orphans
  # Building the new containers.
  docker compose -f ./docker-compose.yml up -d --remove-orphans
}

function run_prod() {
  echo "[STATUS] - Running Production environnnement."

  # We do not remove older containers.
  # Building the new containers.
  docker compose -f ./docker-compose.yml up -d --remove-orphans
}

# Variables :
ENVIRONNMENT="$1"
PROD="production"
DEV="development"
BUNDLE="bundle"

# Initializing project's files.
chmod +x ./scripts/init.sh
./scripts/init.sh

if [[ -n "$ENVIRONNMENT" ]]; then
  if [[ "$ENVIRONNMENT" == "$DEV" ]]; then
    run_dev
  elif [[ "$ENVIRONNMENT" == "$BUNDLE" ]]; then
    run_bundle
  elif [[ "$ENVIRONNMENT" == "$PROD" ]]; then
    run_prod
  fi
else
  run_dev
fi

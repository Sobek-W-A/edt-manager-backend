#!/bin/bash

# Initializing project's files.

./init.sh

# Building containers.
docker compose down -v
docker compose up -d
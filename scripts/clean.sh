#!/bin/bash

delete_pycache() {
    find . -type d -name "__pycache__" -exec rm -rf {} +
    echo "[STATUS] - All __pycache__ folders have been deleted."
}

echo "[STATUS] - Removing temporary files..."

# Deactivating venv
deactivate
rm -r ./app/.venv
rm ./init_db.sql
rm .env

delete_pycache

echo "[STATUS] - Done cleaning !"

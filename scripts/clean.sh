#!/bin/bash

echo "[STATUS] - Removing temporary files..."

rm -r ./app/.venv
rm ./init_db.sql
rm .env

echo "[STATUS] - Done cleaning !"

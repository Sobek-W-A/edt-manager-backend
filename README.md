# edt-manager-backend

A FastAPI application designed to provide data to the frontend app.

## How to install

In order to install the project, a few requirements are needed :

- Docker Compose
- Python 3.12

If these requirements are satisfied, simply execute the build script.

For Windows :

`.\build.ps1`

For Linux-Based systems:

`chmod +x ./build.sh && ./build.sh`

This script will :

- Create random environnment variables.
- Remove any pre-existing containers made with the dockerfiles of the project.
- Create a python virtual environnment.
- Install dependancies inside de venv.
- Activate the environnment in the current terminal.
- Start the server with the uvicorn utility. It has HMR (Hot Module Replacement) for easier develompent.

The docker compose files will give a Postgresql database as well as a Database Explorer called Adminer.
Adminer is reachable on the http://localhost:8080 address.

The documentation of the API is available at the root address of the API. Check the environnment variables to see the port used by the API.

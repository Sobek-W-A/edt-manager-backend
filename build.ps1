# Initializing project's files.
.\scripts\init.ps1

# Removing pre-existing containers
docker-compose -f .\docker-compose_backdev.yml down -v --remove-orphans

# Building the new containers.
docker-compose -f .\docker-compose_backdev.yml up -d --remove-orphans

# Running the application.
.\scripts\run.ps1

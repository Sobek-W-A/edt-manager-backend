function run_dev {
    Write-Host "[STATUS] - Running Development environment."

    # Removing pre-existing containers
    docker compose -f ./docker-compose_backdev.yml down -v --remove-orphans
    # Building the new containers.
    docker compose -f ./docker-compose_backdev.yml up -d --remove-orphans

    # Running the application.
    ./scripts/run.ps1
}

function run_bundle {
    Write-Host "[STATUS] - Running Bundled environment."

    # Removing pre-existing containers
    docker compose -f ./docker-compose.yml down -v --remove-orphans
    # Building the new containers.
    docker compose -f ./docker-compose.yml up -d --remove-orphans
}

function run_prod {
    Write-Host "[STATUS] - Running Production environment."

    # We do not remove older containers.
    # Building the new containers.
    docker compose -f ./docker-compose.yml up -d --remove-orphans
}

# Variables:
$ENVIRONMENT = $args[0]
$PROD = "production"
$DEV = "development"
$BUNDLE = "bundle"

# Initializing project's files.
./scripts/init.ps1

if ($ENVIRONMENT) {
    if ($ENVIRONMENT -eq $DEV) {
        run_dev
    } elseif ($ENVIRONMENT -eq $BUNDLE) {
        run_bundle
    } elseif ($ENVIRONMENT -eq $PROD) {
        run_prod
    }
} else {
    run_dev
}

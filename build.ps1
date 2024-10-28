function Clean-UpStack {
    param (
        [string]$composeFile
    )

    Write-Output "[STATUS] - Cleaning up stack defined in $composeFile"

    # Stop and remove containers, networks, and volumes associated with the specified compose file
    docker compose -f $composeFile down -v --remove-orphans
    # Remove dangling images specific to this compose file (only those not used by other containers)
    docker images -f "dangling=true" -q | ForEach-Object { docker rmi $_ }
    # Remove any anonymous or dangling volumes specific to this stack
    docker volume prune -f
    # Cleaning the older images
    docker rm -f (docker ps -a -q --filter "name=sobekwa") | Out-Null
    docker rmi -f (docker images -q --filter "reference=sobekwa*") | Out-Null

    Write-Output "[STATUS] - Stack cleaned up successfully."
}

function Run-Dev {
    Write-Output "[STATUS] - Running Development environment."

    # Clean up the development stack
    Clean-UpStack "./docker-compose_backdev.yml"

    # Build and start the containers with no cache
    docker compose -f .\docker-compose_backdev.yml build --no-cache
    docker compose -f .\docker-compose_backdev.yml up -d --remove-orphans --force-recreate

    # Run the application script
    Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
    .\scripts\run.ps1
}

function Run-Bundle {
    Write-Output "[STATUS] - Running Bundled environment."

    # Clean up the bundled stack
    Clean-UpStack "./docker-compose.yml"

    # Build and start the containers with no cache
    $cacheBust = (Get-Date -UFormat %s)
    docker compose -f .\docker-compose.yml build --no-cache --build-arg CACHEBUST=$cacheBust
    docker compose -f .\docker-compose.yml up -d --remove-orphans --force-recreate
}

function Run-Prod {
    Write-Output "[STATUS] - Running Production environment."

    # No stack clean-up to retain the production state
    docker compose -f .\docker-compose.yml up -d --remove-orphans
}

# Variables
$environment = $args[0]
$prod = "production"
$dev = "development"
$bundle = "bundle"

# Initializing project's files.
.\scripts\init.ps1

if ($environment) {
    if ($environment -eq $dev) {
        Run-Dev
    } elseif ($environment -eq $bundle) {
        Run-Bundle
    } elseif ($environment -eq $prod) {
        Run-Prod
    }
} else {
    Run-Dev
}

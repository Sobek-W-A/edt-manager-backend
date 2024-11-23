function Delete-PyCache {
    Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" | ForEach-Object {
        Remove-Item -Recurse -Force -Path $_.FullName
    }
    Write-Host "[STATUS] - All __pycache__ folders have been deleted."
}


Write-Host "[STATUS] - Removing temporary files..."

# Deactivating venv
deactivate
Remove-Item -Recurse -Force .\app\.venv
Remove-Item -Force .\init_db.sql
Remove-Item -Force .env

Delete-PyCache

Write-Host "[STATUS] - Done cleaning!"

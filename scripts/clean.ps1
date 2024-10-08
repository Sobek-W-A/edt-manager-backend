Write-Host "[STATUS] - Removing temporary files..."

Remove-Item -Recurse -Force .\app\.venv
Remove-Item -Force .\init_db.sql
Remove-Item -Force .env

Write-Host "[STATUS] - Done cleaning!"

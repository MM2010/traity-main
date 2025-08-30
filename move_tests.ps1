# Script PowerShell per spostare i file di test
Get-ChildItem -Path "test_*.py" | ForEach-Object {
    $destination = Join-Path -Path "TESTS" -ChildPath $_.Name
    Move-Item -Path $_.FullName -Destination $destination
    Write-Host "Spostato: $($_.Name) -> TESTS/"
}

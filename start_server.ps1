$ErrorActionPreference = "Stop"

Write-Host "Starting Metadata Management System..." -ForegroundColor Green

# Set working directory
Set-Location "D:\python\py_opencode\metadata_manager"

# Start Python process in background
$process = Start-Process -FilePath "C:\Python314\python.exe" `
                          -ArgumentList "app.py" `
                          -RedirectStandardOutput "server.log" `
                          -RedirectStandardError "server_error.log" `
                          -WindowStyle Hidden `
                          -PassThru

Write-Host "Server process started with PID: $($process.Id)" -ForegroundColor Yellow

# Wait a moment for startup
Start-Sleep -Seconds 3

# Check if process is still running
$running = Get-Process -Id $process.Id -ErrorAction SilentlyContinue

if ($running) {
    Write-Host "Server is running successfully!" -ForegroundColor Green
    Write-Host "`nAccess the application at:" -ForegroundColor Cyan
    Write-Host "  - Local: http://127.0.0.1:5000" -ForegroundColor White
    Write-Host "  - Network: http://10.178.80.9:5000" -ForegroundColor White
    Write-Host "`nTo stop the server, run: taskkill /PID $($process.Id) /F" -ForegroundColor Yellow
} else {
    Write-Host "Failed to start server. Check server_error.log for details." -ForegroundColor Red
    Get-Content "server_error.log" -Tail 20
}

Write-Host "`nPress any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
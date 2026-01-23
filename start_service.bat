@echo off
echo Starting Metadata Management System...
cd /d D:\python\py_opencode\metadata_manager

start /B C:\Python314\python.exe app.py > server.log 2>&1

echo Server started. Check server.log for details.
echo Access the application at:
echo   - http://127.0.0.1:5000
echo   - http://10.178.80.9:5000
pause
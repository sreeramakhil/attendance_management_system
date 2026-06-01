@echo off
title Blockchain Attendance Startup Script
color 0B
cls

echo =======================================================================
echo         ⛓  WELCOME TO BLOCKCHAIN ATTENDANCE SYSTEM STARTUP  ⛓
echo =======================================================================
echo.
echo [1/4] Compiling Smart Contracts via Truffle...
cd blockchain
call npx truffle compile
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Truffle compilation failed! Make sure you have Truffle installed.
    pause
    exit /b %errorlevel%
)
cd ..

echo.
echo [2/4] Deploying Smart Contract to Ganache (Port 7546)...
cd backend
call .\venv\Scripts\python deploy.py
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Deployment failed! Ensure Ganache is running on port 7546.
    pause
    exit /b %errorlevel%
)
cd ..

echo.
echo [3/4] Starting Flask Backend API Server in a new window...
start "Blockchain Attendance API (Port 5000)" cmd /k "cd backend && call .\venv\Scripts\python app.py"

echo.
echo [4/4] Starting Python Frontend Server on Port 8080 in a new window...
start "Blockchain Attendance Web Server (Port 8080)" cmd /k "cd frontend && python -m http.server 8080"

echo.
echo =======================================================================
echo          🎉 BLOCKCHAIN ATTENDANCE CHANNELS ACTIVE ^& RUNNING! 🎉
echo =======================================================================
echo.
echo  » PC / Admin Portal:  http://localhost:8080/login.html
echo  » Mobile LAN Checkin: http://192.168.0.104:8080/login.html
echo  » Backend API status: http://192.168.0.104:5000/status
echo.
echo  Keep the server windows open. Press any key to exit this startup script...
pause > nul

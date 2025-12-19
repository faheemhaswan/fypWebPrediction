@echo off
title AquaWise ML Backend Server
color 0A
echo ========================================================
echo       AquaWise Smart Irrigation - ML Backend
echo ========================================================
echo.
echo [INFO] Starting the Python API server...
echo [INFO] API Endpoint: http://localhost:5000/predict
echo.
echo [IMPORTANT] KEEP THIS WINDOW OPEN while using the website!
echo.
.\venv\Scripts\python.exe app.py
echo.
echo [ERROR] Server stopped. Check if python is installed or path is correct.
pause

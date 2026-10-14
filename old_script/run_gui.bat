@echo off
echo Starting VALORANT Mature Content Manager GUI...
echo.
python gui_script.py
if errorlevel 1 (
    echo.
    echo Error: Could not start the application.
    echo Make sure Python is installed and in your PATH.
    echo.
    pause
)

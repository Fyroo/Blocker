@echo off
NET SESSION >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo You need to run this script as Administrator.
    pause
    exit /b
)
:: Check if virtual environment exists
if not exist "venv" (
    echo "Setup not completed. Running setup script..."
    call setup_windows.bat
)

:: Activate virtual environment
call venv\Scripts\activate

:: Start the Python program
python src\__main__.py
deactivate
exit /b

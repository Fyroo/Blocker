@echo off
:: Check if virtual environment exists
if not exist "venv" (
    echo "Setup not completed. Running setup script..."
    call setup_windows.bat
)

:: Activate virtual environment
call venv\Scripts\activate

:: Start the Python program
python src\__main__.py
exit /b

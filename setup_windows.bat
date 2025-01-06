@echo off

:: Check if running as administrator
whoami /groups | find "S-1-5-32-544" > nul
if not %errorlevel%==0 (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process -FilePath '%~f0' -Verb runAs"
    exit /b
)

:: Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists.
)

:: Activate virtual environment
echo Installing dependencies...
call venv\Scripts\activate

:: Install dependencies
pip install -r requirements.txt
deactivate
echo Setup completed successfully!
exit /b

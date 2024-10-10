@echo off
REM Mengatur jalur ke virtual environment
set VENV_PATH=D:/Magang/bot-telegram/venv/Scripts/activate.bat
echo Mengatur jalur ke virtual environment: %VENV_PATH%

REM Mengatur jalur ke script Python
set SCRIPT_PATH=D:/Magang/bot-telegram/main.py
echo Mengatur jalur ke script Python: %SCRIPT_PATH%

REM Mengaktifkan virtual environment
echo Mengaktifkan virtual environment...
call "%VENV_PATH%"

REM Menjalankan script Python tanpa jendela terminal
echo Menjalankan bot...
start /B pythonw "%SCRIPT_PATH%"

echo Bot sedang dijalankan...
pause

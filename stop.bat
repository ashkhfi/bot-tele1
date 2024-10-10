@echo off
REM Menghentikan semua proses pythonw.exe
taskkill /F /IM pythonw.exe

REM Opsional: Menampilkan pesan setelah menghentikan proses
echo Semua proses pythonw.exe telah dihentikan.
pause

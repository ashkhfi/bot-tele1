@echo off
REM Menghentikan semua proses pythonw.exe
taskkill /F /IM python.exe

REM Opsional: Menampilkan pesan setelah menghentikan proses
echo Semua proses python.exe telah dihentikan.
pause

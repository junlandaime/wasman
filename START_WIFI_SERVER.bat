@echo off
title Wasman - Akses Wi-Fi Local Server
cls
echo =========================================================
echo      MEMULAI SERVER WASMAN UNTUK AKSES HP / WI-FI
echo =========================================================
echo.
python scripts\serve_wifi.py 8000
if errorlevel 1 (
    echo.
    echo Menjalankan alternatif menggunakan PHP Herd...
    php -S 0.0.0.0:8000 -t mockups
)
pause

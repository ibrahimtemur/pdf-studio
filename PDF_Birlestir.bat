@echo off
title Goruntu - PDF Birlestirici
cd /d "%~dp0"

python --version >nul 2>&1
if %errorlevel% equ 0 (
    python goruntu_pdf.py
    goto end
)

py --version >nul 2>&1
if %errorlevel% equ 0 (
    py goruntu_pdf.py
    goto end
)

echo [HATA] Python bulunamadi!
echo Lutfen Python'un kurulu ve PATH'e ekli oldugundan emin olun.
echo Indirme linki: https://www.python.org/downloads/
echo.
pause

:end
if %errorlevel% neq 0 (
    echo.
    echo Program bir hata ile kapandi.
    pause
)

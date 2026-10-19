@echo off
chcp 65001 >nul
cd /d "%~dp0"
title PDF Studio — Windows Exe Derleyici (PyInstaller)

echo ========================================================
echo        PDF Studio — Windows Exe Derleme Aracı
echo ========================================================
echo.

REM 1. Python Varligini Kontrol Et
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PY_CMD=python"
    goto :has_python
)
py --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PY_CMD=py"
    goto :has_python
)

echo [HATA] Python bulunamadi!
echo Lutfen Python 3.10 veya uzerini kurup PATH ortam degiskenine ekleyin.
echo Indirme: https://www.python.org/downloads/
echo.
pause
exit /b 1

:has_python

REM 2. Sanal Ortami (.venv) Kontrol Et ve Olustur
if not exist ".venv\Scripts\activate.bat" (
    echo [*] .venv sanal ortami bulunamadi, olusturuluyor...
    %PY_CMD% -m venv .venv
    if errorlevel 1 (
        echo [HATA] Sanal ortam olusturulamadi!
        pause
        exit /b 1
    )
    echo [OK] Sanal ortam basariyla olusturuldu.
)

REM 3. Sanal Ortami Aktif Et
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo [HATA] Sanal ortam aktif edilemedi!
    pause
    exit /b 1
)

REM 4. Bagimliliklari ve PyInstaller'i Yukle/Guncelle
echo [*] Bagimliliklar ve PyInstaller kontrol ediliyor / yukleniyor...
python -m pip install --upgrade pip
pip install -r requirements.txt pyinstaller
if errorlevel 1 (
    echo [HATA] Gerekli paketler yuklenirken bir sorun olustu!
    pause
    exit /b 1
)
echo [OK] Tum paketler hazir.
echo.

REM 5. PyInstaller ile Derleme Yap
echo [*] PyInstaller ile tek parca Windows Exe derleniyor...
echo     Parametreler: --onefile --windowed --collect-all customtkinter
echo     Lutfen bekleyin (bu islem 1-3 dakika surebilir)...
echo.

pyinstaller --noconfirm --clean --onefile --windowed --name "PDF-Studio" --icon "assets\icon.ico" --version-file version_info.txt --collect-all customtkinter --add-data "assets;assets" goruntu_pdf.py

if errorlevel 1 (
    echo.
    echo ========================================================
    echo [HATA] Derleme basarisiz oldu!
    echo Lutfen yukaridaki PyInstaller hata loglarini inceleyin.
    echo ========================================================
    pause
    exit /b 1
)

REM 6. Ciktiyi Dogrula ve SHA-256 Hesapla
if not exist "dist\PDF-Studio.exe" (
    echo [HATA] dist\PDF-Studio.exe dosyasi bulunamadi!
    pause
    exit /b 1
)

echo.
echo ========================================================
echo [BASARILI] PDF Studio Exe basariyla olusturuldu!
echo Dosya: dist\PDF-Studio.exe
echo ========================================================
echo.
echo SHA-256 Butunluk Ozeti:
certutil -hashfile "dist\PDF-Studio.exe" SHA256
echo.

REM 7. dist Klasorunu Ac
echo [*] dist klasoru aciliyor...
explorer "dist"

echo.
echo Islem tamamlandi. Pencereyi kapatabilirsiniz.
pause

@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
title PDF Studio — Windows Exe Derleyici (PyInstaller)
cd /d "%~dp0"

echo ========================================================
echo        PDF Studio — Windows Exe Derleme Aracı
echo ========================================================
echo.

:: 1. Python Varlığını Kontrol Et
python --version >nul 2>&1
if %errorlevel% neq 0 (
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [HATA] Python bulunamadı!
        echo Lütfen Python 3.10 veya üzerini kurup PATH ortam değişkenine ekleyin.
        echo İndirme: https://www.python.org/downloads/
        echo.
        pause
        exit /b 1
    )
    set "PY_CMD=py"
) else (
    set "PY_CMD=python"
)

:: 2. Sanal Ortamı (.venv) Kontrol Et ve Oluştur
if not exist ".venv\Scripts\activate.bat" (
    echo [*] .venv sanal ortamı bulunamadı, oluşturuluyor...
    %PY_CMD% -m venv .venv
    if %errorlevel% neq 0 (
        echo [HATA] Sanal ortam oluşturulamadı!
        pause
        exit /b %errorlevel%
    )
    echo [OK] Sanal ortam başarıyla oluşturuldu.
)

:: 3. Sanal Ortamı Aktif Et
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [HATA] Sanal ortam aktif edilemedi!
    pause
    exit /b %errorlevel%
)

:: 4. Bağımlılıkları ve PyInstaller'ı Yükle/Güncelle
echo [*] Bağımlılıklar ve PyInstaller kontrol ediliyor / yükleniyor...
python -m pip install --upgrade pip
pip install -r requirements.txt pyinstaller
if %errorlevel% neq 0 (
    echo [HATA] Gerekli paketler yüklenirken bir sorun oluştu!
    pause
    exit /b %errorlevel%
)
echo [OK] Tüm paketler hazır.
echo.

:: 5. PyInstaller ile Derleme Yap
echo [*] PyInstaller ile tek parça Windows Exe derleniyor...
echo     Parametreler: --onefile --windowed --collect-all customtkinter
echo     Lütfen bekleyin (bu işlem 1-3 dakika sürebilir)...
echo.

pyinstaller --noconfirm --clean --onefile --windowed ^
    --name "PDF-Studio" ^
    --icon "assets\icon.ico" ^
    --version-file version_info.txt ^
    --collect-all customtkinter ^
    --add-data "assets;assets" ^
    goruntu_pdf.py

if %errorlevel% neq 0 (
    echo.
    echo ========================================================
    echo [HATA] Derleme başarısız oldu!
    echo Lütfen yukarıdaki PyInstaller hata loglarını inceleyin.
    echo ========================================================
    pause
    exit /b %errorlevel%
)

:: 6. Çıktıyı Doğrula ve SHA-256 Hesapla
if not exist "dist\PDF-Studio.exe" (
    echo [HATA] dist\PDF-Studio.exe dosyası bulunamadı!
    pause
    exit /b 1
)

echo.
echo ========================================================
echo [BAŞARILI] PDF Studio Exe başarıyla oluşturuldu!
echo Dosya: dist\PDF-Studio.exe
echo ========================================================
echo.
echo SHA-256 Bütünlük Özeti:
certutil -hashfile "dist\PDF-Studio.exe" SHA256
echo.

:: 7. dist Klasörünü Aç
echo [*] dist klasörü açılıyor...
explorer "dist"

echo.
echo İşlem tamamlandı. Pencereyi kapatabilirsiniz.
pause

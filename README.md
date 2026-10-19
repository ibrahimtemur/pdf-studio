# ⚡ PDF Studio — Image & PDF Merger

<div align="center">

[![GitHub Release](https://img.shields.io/github/v/release/ibrahimtemur/pdf-studio?style=for-the-badge&color=blue&logo=github)](https://github.com/ibrahimtemur/pdf-studio/releases/latest)
[![Platform Windows](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://github.com/ibrahimtemur/pdf-studio/releases/latest)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<br/>

**A modern, blazing fast, and elegant Windows desktop application that combines all images (`.png`, `.jpg`, `.jpeg`, `.bmp`, `.tiff`, `.webp`) and existing `.pdf` files in a folder into a single unified PDF document using natural human sorting.**

<br/>

<a href="https://github.com/ibrahimtemur/pdf-studio/releases/latest">
  <img src="https://img.shields.io/badge/⬇️_Download_Now-PDF--Studio--Windows.exe-4f46e5?style=for-the-badge&logo=windows&logoColor=white" height="42" alt="Download Now">
</a>

<p align="center"><sub>(No Python or external runtime installation required — Just download and double-click!)</sub></p>

[Türkçe Dokümantasyon](README.tr.md) • [Quick Start](#-quick-start) • [Features](#-features) • [FAQ](#-frequently-asked-questions-faq) • [Developers](#%EF%B8%8F-for-developers)

</div>

---

## ✨ Features

- **🎨 Modern Dark UI:** CustomTkinter-powered sleek dark mode with high-contrast card layout.
- **🖼️ Multi-Format Support:** Seamlessly merge PNG, JPG, JPEG, BMP, TIFF, TIF, WEBP, and PDF documents in one pass.
- **🔢 Natural Sorting:** Files are ordered intelligently (`1, 2, 10` instead of alphabetical `1, 10, 2`).
- **📐 Smart Page Orientation:** Landscape or Portrait A4 options, proportional image fitting, and automatic 90° orientation adjustment.
- **🎚️ Adjustable JPEG Quality:** Live slider from 40% to 100% to easily control file output size.
- **⚡ Instant Folder Scanning:** Real-time feedback displaying the exact count of images and PDFs upon folder selection.
- **📊 Live Progress & Logging:** Real-time progress bar, page counter, detailed log console, and direct buttons to open the merged PDF or output folder.
- **🛡️ Robust & Crash-Proof:** Comprehensive logging to `%LOCALAPPDATA%\PDFStudio\error.log` and seamless frozen executable (`sys.frozen`) support.

---

## 🚀 Quick Start

Choose between two easy ways to run PDF Studio:

### Option A (Recommended): Pre-Built Windows `.exe`
> **No Python or setup tools required.**

1. Visit the [GitHub Releases Latest Page](https://github.com/ibrahimtemur/pdf-studio/releases/latest).
2. Download the latest `PDF-Studio-v...-Windows.exe`.
3. Double-click the downloaded executable to launch the app!
4. *(Optional)* Verify file integrity in PowerShell:
   ```cmd
   certutil -hashfile "PDF-Studio-v1.0.0-Windows.exe" SHA256
   ```
   Compare the resulting checksum with the provided `.sha256` asset.

---

### Option B: Run from Source Code via `.bat`
> For developers or users with Python already installed.

1. Clone or download the repository: Click the green **Code** button and select **Download ZIP**, then extract it.
2. Double-click `PDF_Birlestir.bat` in the root folder.
3. The script detects your local Python installation, automatically checks and installs any missing libraries (`customtkinter`, `Pillow`, `fpdf2`, `pypdf`), and starts the application.

---

## ❓ Frequently Asked Questions (FAQ)

### 1. Windows SmartScreen displays "Unknown Publisher", what should I do?
- **Why does this appear?** PDF Studio is a free, open-source project. Microsoft SmartScreen displays this prompt for any newly released executable without an expensive corporate Extended Validation (EV) Code Signing certificate. This does **not** indicate malicious software.
- **How to proceed:**
  1. In the blue Windows SmartScreen popup, click **More info** (Ek Bilgi).
  2. Click **Run anyway** (Yine de Çalıştır). The application will launch normally.

### 2. My Antivirus flagged the executable, is it safe?
- Standalone PyInstaller (`--onefile`) executables unpack runtime dependencies to a temporary folder (`%TEMP%`) on launch. Some antivirus heuristics can generate false-positive alerts on generic binary wrappers.
- The project is **100% open source**. You can inspect the entire Python code in [goruntu_pdf.py](goruntu_pdf.py).
- You can verify the official SHA-256 hash using `certutil -hashfile ... SHA256` or build the binary yourself using `build_exe.bat`.

### 3. Why does the application take a few seconds to launch on first run?
- The single-file executable extracts bundled resources and theme assets into a temporary sandbox in memory/disk upon launch. Depending on your storage drive speed, initial startup may take 2 to 4 seconds. Subsequent operations are instant.

### 4. Can I customize the window/application icon?
- Absolutely! Replace [assets/icon.ico](assets/icon.ico) with your own multi-resolution `.ico` file and run `build_exe.bat` to recompile with your brand logo.

---

## 🛠️ For Developers

### Building the Executable Locally (`build_exe.bat`)
If you have Python 3.10+ installed on Windows, you can compile with a single click:

1. Double-click `build_exe.bat` in the project root.
2. The batch script will automatically:
   - Create or verify the `.venv` virtual environment.
   - Install `requirements.txt` and `pyinstaller`.
   - Bundle `version_info.txt`, `assets/icon.ico`, and CustomTkinter theme assets.
   - Generate `dist\PDF-Studio.exe`, print its SHA-256 hash, and open the `dist\` folder.

Manual build command:
```cmd
pyinstaller --noconfirm --clean --onefile --windowed ^
  --name "PDF-Studio" ^
  --icon "assets\icon.ico" ^
  --version-file version_info.txt ^
  --collect-all customtkinter ^
  --add-data "assets;assets" ^
  goruntu_pdf.py
```

### Publishing Releases via GitHub Actions
When you push a version tag to GitHub, the CI/CD pipeline builds the Windows executable, computes the SHA-256 checksum, and drafts a complete GitHub Release:

```bash
git tag v1.0.1
git push origin v1.0.1
```

You can also trigger builds manually anytime using the **Run workflow** (`workflow_dispatch`) button in the Actions tab.

---

## 📁 Project Structure

```
goruntu-pdf-birlestirici/
├── .github/
│   └── workflows/
│       └── release.yml          # Automated GitHub Actions CI/CD release workflow
├── assets/
│   └── icon.ico                 # Multi-resolution application icon (16px..256px)
├── .gitattributes               # Line endings and binary file handling rules
├── .gitignore                   # Exclusions for PyInstaller, venv, and IDEs
├── build_exe.bat                # Windows one-click PyInstaller build script
├── goruntu_pdf.py               # Main application source code (CustomTkinter)
├── LICENSE                      # MIT Open Source License
├── PDF_Birlestir.bat            # Alternative launcher from Python source
├── README.md                    # English documentation
├── README.tr.md                 # Turkish documentation
├── requirements.txt             # Python dependencies
└── version_info.txt             # Windows Exe VERSIONINFO metadata
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute it.

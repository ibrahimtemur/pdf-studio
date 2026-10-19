# ⚡ PDF Studio — Görüntü ve PDF Birleştirici

<div align="center">

[![GitHub Release](https://img.shields.io/github/v/release/ibrahimtemur/pdf-studio?style=for-the-badge&color=blue&logo=github)](https://github.com/ibrahimtemur/pdf-studio/releases/latest)
[![Platform Windows](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://github.com/ibrahimtemur/pdf-studio/releases/latest)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<br/>

**Bir klasördeki tüm görselleri (`.png`, `.jpg`, `.jpeg`, `.bmp`, `.tiff`, `.webp`) ve mevcut `.pdf` belgelerini doğal sıralama mantığıyla tek bir PDF dosyasında birleştiren modern, hızlı ve şık Windows masaüstü uygulaması.**

<br/>

<a href="https://github.com/ibrahimtemur/pdf-studio/releases/latest">
  <img src="https://img.shields.io/badge/⬇️_Hemen_İndir-PDF--Studio--Windows.exe-4f46e5?style=for-the-badge&logo=windows&logoColor=white" height="42" alt="Hemen İndir">
</a>

<p align="center"><sub>(Python veya herhangi bir kurulum gerektirmez — İndirin ve çift tıklayın!)</sub></p>

[English Documentation](README.md) • [Hızlı Başlangıç](#-hızlı-başlangıç) • [Özellikler](#-özellikler) • [SSS](#-sıkça-sorulan-sorular-sss) • [Geliştiriciler](#%EF%B8%8F-geliştiriciler-için)

</div>

---

## ✨ Özellikler

- **🎨 Modern Dark UI:** CustomTkinter tabanlı, göz yormayan karanlık tema ve şık kart tasarımı.
- **🖼️ Çoklu Format Desteği:** PNG, JPG, JPEG, BMP, TIFF, TIF, WEBP ve PDF dosyalarını tek işlemde harmanlar.
- **🔢 İnsan Mantığına Uygun Sıralama (Natural Sort):** Dosyaları `1, 2, 10` şeklinde sıralar (`1, 10, 2` karmaşasını önler).
- **📐 Akıllı Sayfa Yönlendirme:** Yatay (Landscape) veya Dikey (Portrait) A4 modları, görselleri orantılı sığdırma ve otomatik 90° döndürme.
- **🎚️ Ayarlanabilir JPEG Kalitesi:** Çıktı dosya boyutunu kontrol etmek için %40 ile %100 arasında canlı kalite seçici.
- **⚡ Canlı Klasör Taraması:** Kaynak klasör seçildiği an toplam kaç görsel ve kaç PDF bulunduğunu ekranda anında gösterir.
- **📊 Ayrıntılı İlerleme ve Günlük:** Gerçek zamanlı işlem çubuğu, sayfa sayacı, konsol günlüğü ve işlem bitiminde doğrudan PDF'i / çıktı klasörünü açma butonları.
- **🛡️ Kararlı ve Güvenli:** Hataları yutmayan küresel loglama (`%LOCALAPPDATA%\PDFStudio\error.log`) ve donmuş exe (`sys.frozen`) uyumluluğu.

---

## 🚀 Hızlı Başlangıç

Uygulamayı kullanmak için iki kolay yol bulunmaktadır:

### Seçenek A (Önerilen): Hazır Windows `.exe` Dosyası
> **Python veya ek hiçbir araç kurmanıza gerek yoktur.**

1. [GitHub Releases En Son Sürüm](https://github.com/ibrahimtemur/pdf-studio/releases/latest) sayfasına gidin.
2. `PDF-Studio-v...-Windows.exe` dosyasını bilgisayarınıza indirin.
3. İndirdiğiniz `.exe` dosyasına çift tıklayarak uygulamayı başlatın.
4. *(İsteğe bağlı)* Dosya bütünlüğünü doğrulamak için PowerShell'de:
   ```cmd
   certutil -hashfile "PDF-Studio-v1.0.0-Windows.exe" SHA256
   ```
   Çıkan hash değerini Releases sayfasındaki `.sha256` dosyasıyla karşılaştırın.

---

### Seçenek B: `.bat` ile Kaynak Koddan Çalıştırma
> Python yüklü ortamlarda kaynak koddan çalıştırmak isteyenler içindir.

1. Depoyu indirin: Sağ üstteki yeşil **Code** butonuna basıp **Download ZIP** seçeneğini kullanın ve klasöre çıkarın (veya `git clone` yapın).
2. Klasör içerisindeki `PDF_Birlestir.bat` dosyasına çift tıklayın.
3. Betik, sisteminizdeki Python kurulumunu algılar; gerekli kütüphaneler (`customtkinter`, `Pillow`, `fpdf2`, `pypdf`) eksikse bunları ilk açılışta otomatik olarak yükler ve uygulamayı başlatır.

---

## ❓ Sıkça Sorulan Sorular (SSS)

### 1. Windows SmartScreen "Bilinmeyen Yayıncı" uyarısı veriyor, ne yapmalıyım?
- **Neden Çıkar?** PDF Studio açık kaynaklı ve bağımsız bir projedir. Microsoft'un SmartScreen filtresi, yıllık yüzlerce dolar maliyeti olan kurumsal dijital kod imzalama (EV Code Signing) sertifikasına sahip olmayan yeni `.exe` dosyalarında bu uyarıyı standart olarak gösterir. Bu durum uygulamanın zararlı olduğu anlamına **gelmez**.
- **Nasıl Geçilir?**
  1. Açılan mavi SmartScreen penceresinde **Ek Bilgi** (More Info) bağlantısına tıklayın.
  2. Altta beliren **Yine de Çalıştır** (Run anyway) butonuna tıklayın. Uygulama hemen açılacaktır.

### 2. Antivirüs programım uyarı verdi, bu güvenli mi?
- PyInstaller tek dosya (`--onefile`) derlemeleri, çalışma anında dosyaları geçici klasöre (`%TEMP%`) açtığı için bazı antivirüs motorları tarafından genel sezgisel (heuristics) kalıplarla yanlışlıkla "şüpheli" (false positive) olarak etiketlenebilir.
- Projemiz **%100 açık kaynaklıdır**. Tüm Python kaynak kodunu [goruntu_pdf.py](goruntu_pdf.py) dosyasından bizzat inceleyebilirsiniz.
- Dilerseniz Releases'tan indirdiğiniz dosyanın hash özetini doğrulayabilir (`certutil -hashfile ... SHA256`) veya depoyu klonlayıp kendi bilgisayarınızda `build_exe.bat` betiğiyle doğrudan kendiniz derleyebilirsiniz.

### 3. Exe'ye tıkladıktan sonra açılması neden birkaç saniye sürüyor?
- Uygulama tek bir bağımsız dosya (`--onefile`) olarak paketlenmiştir. Çift tıkladığınızda Windows arkada gerekli CustomTkinter tema varlıklarını ve kütüphaneleri geçici alana açar. Bu nedenle ilk açılış sistemi donanımınıza bağlı olarak 2-4 saniye sürebilir; bu durum tamamen normaldir.

### 4. Uygulamanın ikonunu değiştirebilir miyim?
- Evet! [assets/icon.ico](assets/icon.ico) dosyasının yerine kendi çok boyutlu `.ico` dosyanızı koyup `build_exe.bat` betiğini çalıştırarak kendi özel logonuzla derleme yapabilirsiniz.

---

## 🛠️ Geliştiriciler İçin

### Yerel Ortamda Exe Derleme (`build_exe.bat`)
Bilgisayarınızda Python 3.10+ kuruluysa tek tıkla derleme yapabilirsiniz:

1. Proje ana dizinindeki `build_exe.bat` dosyasına çift tıklayın.
2. Betik otomatik olarak:
   - `.venv` sanal ortamını hazırlar.
   - `requirements.txt` ve `pyinstaller` paketlerini kurar.
   - `version_info.txt`, `assets/icon.ico` ve CustomTkinter varlıklarını dahil ederek derler.
   - `dist\PDF-Studio.exe` dosyasını oluşturup SHA-256 hash'ini ekrana yazdırır ve `dist\` klasörünü açar.

Manuel derleme komutu:
```cmd
pyinstaller --noconfirm --clean --onefile --windowed ^
  --name "PDF-Studio" ^
  --icon "assets\icon.ico" ^
  --version-file version_info.txt ^
  --collect-all customtkinter ^
  --add-data "assets;assets" ^
  goruntu_pdf.py
```

### GitHub Actions ile Yeni Sürüm Yayınlama
Depoya yeni bir Git etiketi (tag) push edildiğinde, GitHub Actions Windows koşucusu üzerinde derlemeyi otomatik olarak yapar, SHA-256 dosyası üretir ve Releases sayfasına yükler:

```bash
git tag v1.0.1
git push origin v1.0.1
```

Ayrıca GitHub Actions sekmesinden **"Release PDF Studio Windows Exe"** iş akışını dilediğiniz zaman `workflow_dispatch` butonu ile manuel olarak da tetikleyebilirsiniz.

---

## 📁 Proje Yapısı

```
goruntu-pdf-birlestirici/
├── .github/
│   └── workflows/
│       └── release.yml          # Otomatik GitHub Releases CI/CD iş akışı
├── assets/
│   └── icon.ico                 # Uygulama ve pencere ikonu (16px..256px)
├── .gitattributes               # Git satır sonu ve ikili dosya kuralları
├── .gitignore                   # PyInstaller, sanal ortam ve IDE yoksaymaları
├── build_exe.bat                # Windows tek tıkla PyInstaller derleme betiği
├── goruntu_pdf.py               # Ana uygulama kaynak kodu (CustomTkinter)
├── LICENSE                      # MIT Açık Kaynak Lisansı
├── PDF_Birlestir.bat            # Kaynak koddan alternatif başlatıcı
├── README.md                    # İngilizce dokümantasyon
├── README.tr.md                 # Türkçe dokümantasyon
├── requirements.txt             # Python bağımlılıkları listesi
└── version_info.txt             # Windows Exe Özellikler/Sürüm meta verisi
```

---

## 📄 Lisans

Bu proje [MIT Lisansı](LICENSE) kapsamında korunmaktadır. Özgürce kullanabilir, değiştirebilir ve dağıtabilirsiniz.

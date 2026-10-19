import os
import sys
import tempfile
import shutil
import threading
import re
import subprocess
import traceback
import time
import tkinter as tk
from tkinter import filedialog, messagebox

# ── Yardımcı Yollar ve Donmuş (Frozen) Exe Desteği ────────────────────────────
def resource_path(relative_path):
    """PyInstaller ile paketlenmiş veya normal çalışma durumunda dosya yolunu döner."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


# ── Global Hata Yakalayıcı (Exception Handler) ────────────────────────────────
def global_exception_handler(exc_type, exc_value, exc_traceback):
    """Yakalanmamış tüm istisnaları loglar ve kullanıcıya hata penceresi gösterir."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    err_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))

    # %LOCALAPPDATA%\PDFStudio\error.log dosyasına yaz
    try:
        local_app_data = os.environ.get("LOCALAPPDATA", os.path.expanduser("~"))
        log_dir = os.path.join(local_app_data, "PDFStudio")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "error.log")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\n--- Hata Raporu ({time.strftime('%Y-%m-%d %H:%M:%S')}) ---\n")
            f.write(err_msg)
    except Exception:
        pass

    # Kullanıcıya görsel uyarı ver
    try:
        messagebox.showerror(
            "Kritik Hata — PDF Studio",
            f"Beklenmeyen bir hata oluştu:\n\n{exc_value}\n\nAyrıntılar günlük dosyasına yazıldı:\n%LOCALAPPDATA%\\PDFStudio\\error.log"
        )
    except Exception:
        pass


sys.excepthook = global_exception_handler
tk.Tk.report_callback_exception = lambda self, exc, val, tb: global_exception_handler(exc, val, tb)

# ── Otomatik Bağımlılık Kontrolü (Sadece kaynak koddan çalışırken) ────────────
if not getattr(sys, "frozen", False):
    for pkg, import_name in [
        ("customtkinter", "customtkinter"),
        ("Pillow", "PIL"),
        ("fpdf2", "fpdf"),
        ("pypdf", "pypdf"),
    ]:
        try:
            __import__(import_name)
        except ImportError:
            print(f"Gerekli kütüphane yükleniyor: {pkg}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])

import customtkinter as ctk
from PIL import Image
from fpdf import FPDF
from pypdf import PdfWriter, PdfReader

# ── Sabitler ve Desteklenen Formatlar ─────────────────────────────────────────
GORUNTU_UZANTILARI = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif', '.webp')
DESTEKLI_UZANTILAR = GORUNTU_UZANTILARI + ('.pdf',)


def natural_sort_key(s):
    """Dosyaları insan mantığına uygun (1, 2, 10 şeklinde) sıralar."""
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', s)]


# ── Görünüm Ayarları ──────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ModernPdfBirlestirici(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PDF Studio — Görüntü ve PDF Birleştirici")
        self.geometry("740x840")
        self.minsize(680, 780)

        # Durum değişkenleri
        self.kaynak_klasor = tk.StringVar()
        self.pdf_adi = tk.StringVar(value="Birlestirilmis_Belge")
        self.kayit_klasor = tk.StringVar(value=os.path.expanduser("~\\Documents"))
        self.yon = tk.StringVar(value="Yatay (Landscape)")
        self.kalite = tk.IntVar(value=90)
        self.calisiyor = False
        self.olusturulan_pdf = None

        self._pencereyi_ortala(740, 840)
        self._arayuz_olustur()
        self.after(200, self._ikon_ayarla)

    def _ikon_ayarla(self):
        """Pencere ikonu için assets/icon.ico dosyasını yükler."""
        try:
            ico_yolu = resource_path(os.path.join("assets", "icon.ico"))
            if os.path.exists(ico_yolu):
                self.iconbitmap(ico_yolu)
        except Exception:
            pass

    def _pencereyi_ortala(self, w, h):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = max(0, (sw - w) // 2)
        y = max(0, (sh - h) // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _arayuz_olustur(self):
        # Ana taşıyıcı scrollable frame
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=20, pady=16)

        # ── 1. HEADER (Başlık Alanı) ────────────────────────────────────────
        header = ctk.CTkFrame(self.scroll, fg_color="#1e293b", corner_radius=14, border_width=1, border_color="#334155")
        header.pack(fill="x", pady=(0, 14), ipady=6)

        head_inner = ctk.CTkFrame(header, fg_color="transparent")
        head_inner.pack(fill="x", padx=18, pady=12)

        icon_title = ctk.CTkFrame(head_inner, fg_color="transparent")
        icon_title.pack(side="left")

        ctk.CTkLabel(icon_title, text="⚡ PDF Studio", font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
                     text_color="#f8fafc").pack(anchor="w")
        ctk.CTkLabel(icon_title, text="Klasördeki tüm görselleri ve PDF'leri tek bir belgede birleştirin",
                     font=ctk.CTkFont(family="Segoe UI", size=12), text_color="#94a3b8").pack(anchor="w")

        badge = ctk.CTkLabel(head_inner, text="v2.0 Modern", fg_color="#3b82f6", corner_radius=8,
                             font=ctk.CTkFont(size=11, weight="bold"), text_color="#ffffff", padx=10, pady=4)
        badge.pack(side="right")

        # ── 2. KAYNAK KLASÖR KARTI ──────────────────────────────────────────
        f_kaynak = ctk.CTkFrame(self.scroll, fg_color="#1e293b", corner_radius=12, border_width=1, border_color="#334155")
        f_kaynak.pack(fill="x", pady=6, padx=2)

        ctk.CTkLabel(f_kaynak, text="📁  Kaynak Klasör", font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
                     text_color="#38bdf8").pack(anchor="w", padx=16, pady=(12, 4))

        k_row = ctk.CTkFrame(f_kaynak, fg_color="transparent")
        k_row.pack(fill="x", padx=16, pady=(0, 6))

        self.entry_kaynak = ctk.CTkEntry(k_row, textvariable=self.kaynak_klasor, placeholder_text="Görüntü ve PDF'lerin bulunduğu klasörü seçin...",
                                         height=38, font=ctk.CTkFont(size=12), fg_color="#0f172a", border_color="#334155")
        self.entry_kaynak.pack(side="left", fill="x", expand=True, padx=(0, 10))

        btn_kaynak = ctk.CTkButton(k_row, text="Gözat...", width=90, height=38, font=ctk.CTkFont(weight="bold"),
                                   fg_color="#0284c7", hover_color="#0369a1", command=self._kaynak_sec)
        btn_kaynak.pack(side="right")

        # Canlı klasör tarama bilgisi
        self.lbl_tarama = ctk.CTkLabel(f_kaynak, text="ℹ️ Henüz klasör seçilmedi",
                                       font=ctk.CTkFont(size=11), text_color="#94a3b8")
        self.lbl_tarama.pack(anchor="w", padx=16, pady=(0, 10))

        # ── 3. ÇIKTI AYARLARI KARTI ─────────────────────────────────────────
        f_cikis = ctk.CTkFrame(self.scroll, fg_color="#1e293b", corner_radius=12, border_width=1, border_color="#334155")
        f_cikis.pack(fill="x", pady=6, padx=2)

        ctk.CTkLabel(f_cikis, text="💾  Çıktı Dosyası ve Konumu", font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
                     text_color="#38bdf8").pack(anchor="w", padx=16, pady=(12, 4))

        # PDF Adı
        ctk.CTkLabel(f_cikis, text="Oluşturulacak PDF Adı:", font=ctk.CTkFont(size=12), text_color="#cbd5e1").pack(anchor="w", padx=16)
        self.entry_ad = ctk.CTkEntry(f_cikis, textvariable=self.pdf_adi, height=38, font=ctk.CTkFont(size=12),
                                     fg_color="#0f172a", border_color="#334155")
        self.entry_ad.pack(fill="x", padx=16, pady=(2, 10))

        # Kayıt Klasörü
        ctk.CTkLabel(f_cikis, text="Kaydedilecek Klasör:", font=ctk.CTkFont(size=12), text_color="#cbd5e1").pack(anchor="w", padx=16)
        c_row = ctk.CTkFrame(f_cikis, fg_color="transparent")
        c_row.pack(fill="x", padx=16, pady=(2, 12))

        self.entry_kayit = ctk.CTkEntry(c_row, textvariable=self.kayit_klasor, height=38, font=ctk.CTkFont(size=12),
                                        fg_color="#0f172a", border_color="#334155")
        self.entry_kayit.pack(side="left", fill="x", expand=True, padx=(0, 10))

        btn_kayit = ctk.CTkButton(c_row, text="Gözat...", width=90, height=38, font=ctk.CTkFont(weight="bold"),
                                  fg_color="#334155", hover_color="#475569", command=self._kayit_sec)
        btn_kayit.pack(side="right")

        # ── 4. SAYFA & KALİTE AYARLARI KARTI ────────────────────────────────
        f_opt = ctk.CTkFrame(self.scroll, fg_color="#1e293b", corner_radius=12, border_width=1, border_color="#334155")
        f_opt.pack(fill="x", pady=6, padx=2)

        ctk.CTkLabel(f_opt, text="⚙️  Görüntü ve Sayfa Seçenekleri", font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
                     text_color="#38bdf8").pack(anchor="w", padx=16, pady=(12, 8))

        opt_grid = ctk.CTkFrame(f_opt, fg_color="transparent")
        opt_grid.pack(fill="x", padx=16, pady=(0, 14))

        # Yön seçici
        ctk.CTkLabel(opt_grid, text="Sayfa Yönü (Görseller için):", font=ctk.CTkFont(size=12),
                     text_color="#cbd5e1").pack(anchor="w", pady=(0, 4))
        self.seg_yon = ctk.CTkSegmentedButton(opt_grid, values=["Yatay (Landscape)", "Dikey (Portrait)"],
                                             variable=self.yon, height=34, font=ctk.CTkFont(size=12),
                                             selected_color="#4f46e5", selected_hover_color="#4338ca")
        self.seg_yon.pack(fill="x", pady=(0, 12))

        # Kalite Slider
        kal_head = ctk.CTkFrame(opt_grid, fg_color="transparent")
        kal_head.pack(fill="x")
        ctk.CTkLabel(kal_head, text="JPEG Görsel Kalitesi:", font=ctk.CTkFont(size=12),
                     text_color="#cbd5e1").pack(side="left")
        self.lbl_kalite_val = ctk.CTkLabel(kal_head, text="90%", font=ctk.CTkFont(size=12, weight="bold"),
                                           text_color="#38bdf8")
        self.lbl_kalite_val.pack(side="right")

        self.slider_kalite = ctk.CTkSlider(opt_grid, from_=40, to=100, number_of_steps=60,
                                           variable=self.kalite, height=18,
                                           progress_color="#4f46e5", button_color="#818cf8", button_hover_color="#a5b4fc",
                                           command=lambda v: self.lbl_kalite_val.configure(text=f"{int(v)}%"))
        self.slider_kalite.pack(fill="x", pady=(4, 0))

        # ── 5. İŞLEM BUTONU & İLERLEME KARTI ────────────────────────────────
        f_action = ctk.CTkFrame(self.scroll, fg_color="#1e293b", corner_radius=12, border_width=1, border_color="#334155")
        f_action.pack(fill="x", pady=6, padx=2)

        self.btn_islem = ctk.CTkButton(f_action, text="🚀  PDF Oluştur ve Birleştir",
                                       height=48, font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
                                       fg_color="#4f46e5", hover_color="#4338ca", corner_radius=10,
                                       command=self._baslat)
        self.btn_islem.pack(fill="x", padx=16, pady=(16, 10))

        # İlerleme Çubuğu ve Durum
        self.prog_bar = ctk.CTkProgressBar(f_action, height=10, corner_radius=5, progress_color="#10b981")
        self.prog_bar.set(0)
        self.prog_bar.pack(fill="x", padx=16, pady=(0, 6))

        self.lbl_durum = ctk.CTkLabel(f_action, text="Hazır", font=ctk.CTkFont(size=12), text_color="#94a3b8")
        self.lbl_durum.pack(anchor="w", padx=16, pady=(0, 6))

        # Hızlı Açma Butonları (Tamamlandığında aktifleşir)
        self.f_tamam_butonlar = ctk.CTkFrame(f_action, fg_color="transparent")
        self.f_tamam_butonlar.pack(fill="x", padx=16, pady=(0, 12))

        self.btn_ac_pdf = ctk.CTkButton(self.f_tamam_butonlar, text="📄  Oluşturulan PDF'i Aç",
                                        height=36, font=ctk.CTkFont(size=12, weight="bold"),
                                        fg_color="#059669", hover_color="#047857",
                                        command=self._pdf_ac, state="disabled")
        self.btn_ac_pdf.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self.btn_ac_klasor = ctk.CTkButton(self.f_tamam_butonlar, text="📂  Klasörü Göster",
                                           height=36, font=ctk.CTkFont(size=12, weight="bold"),
                                           fg_color="#334155", hover_color="#475569",
                                           command=self._klasor_ac, state="disabled")
        self.btn_ac_klasor.pack(side="right", fill="x", expand=True, padx=(6, 0))

        # ── 6. İŞLEM GÜNLÜĞÜ (LOG BOX) ───────────────────────────────────────
        f_log = ctk.CTkFrame(self.scroll, fg_color="#1e293b", corner_radius=12, border_width=1, border_color="#334155")
        f_log.pack(fill="both", expand=True, pady=6, padx=2)

        log_head = ctk.CTkFrame(f_log, fg_color="transparent")
        log_head.pack(fill="x", padx=16, pady=(10, 4))
        ctk.CTkLabel(log_head, text="📋  İşlem Günlüğü", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color="#cbd5e1").pack(side="left")

        btn_temizle = ctk.CTkButton(log_head, text="Temizle", width=60, height=24, font=ctk.CTkFont(size=10),
                                    fg_color="#334155", hover_color="#475569", command=self._log_temizle)
        btn_temizle.pack(side="right")

        self.txt_log = ctk.CTkTextbox(f_log, height=130, font=ctk.CTkFont(family="Consolas", size=11),
                                      fg_color="#090d16", text_color="#cbd5e1", corner_radius=8,
                                      border_width=1, border_color="#1e293b")
        self.txt_log.pack(fill="both", expand=True, padx=16, pady=(0, 14))

    # ── Yardımcı Fonksiyonlar ────────────────────────────────────────────────
    def _kaynak_sec(self):
        klasor = filedialog.askdirectory(title="Görüntü ve PDF Klasörünü Seçin")
        if klasor:
            self.kaynak_klasor.set(klasor)
            self._klasor_tara(klasor)

    def _kayit_sec(self):
        klasor = filedialog.askdirectory(title="PDF'in Kaydedileceği Klasörü Seçin")
        if klasor:
            self.kayit_klasor.set(klasor)

    def _klasor_tara(self, kaynak):
        """Klasördeki dosya sayılarını anında tespit edip kullanıcıya bildirir."""
        if not os.path.isdir(kaynak):
            return

        try:
            butun_dosyalar = os.listdir(kaynak)
            gorseller = [f for f in butun_dosyalar if os.path.splitext(f)[1].lower() in GORUNTU_UZANTILARI]
            pdfler = [f for f in butun_dosyalar if os.path.splitext(f)[1].lower() == '.pdf']
            toplam = len(gorseller) + len(pdfler)

            if toplam > 0:
                self.lbl_tarama.configure(
                    text=f"✔ {toplam} dosya hazır: {len(gorseller)} Görsel, {len(pdfler)} PDF belgesi",
                    text_color="#10b981"
                )
            else:
                self.lbl_tarama.configure(
                    text="⚠️ Bu klasörde desteklenen görüntü veya PDF bulunamadı!",
                    text_color="#f59e0b"
                )
        except Exception as e:
            self.lbl_tarama.configure(text=f"Hata: {e}", text_color="#ef4444")

    def _log(self, mesaj):
        self.txt_log.insert("end", mesaj + "\n")
        self.txt_log.see("end")

    def _log_temizle(self):
        self.txt_log.delete("1.0", "end")

    def _pdf_ac(self):
        if self.olusturulan_pdf and os.path.exists(self.olusturulan_pdf):
            os.startfile(self.olusturulan_pdf)

    def _klasor_ac(self):
        if self.olusturulan_pdf and os.path.exists(self.olusturulan_pdf):
            os.startfile(os.path.dirname(self.olusturulan_pdf))

    def _baslat(self):
        if self.calisiyor:
            return

        kaynak = self.kaynak_klasor.get().strip()
        ad = self.pdf_adi.get().strip()
        kayit = self.kayit_klasor.get().strip()

        if not kaynak or not os.path.isdir(kaynak):
            messagebox.showerror("Eksik Bilgi", "Lütfen geçerli bir kaynak klasör seçin.")
            return

        if not ad:
            messagebox.showerror("Eksik Bilgi", "PDF adı boş bırakılamaz.")
            return

        if not kayit or not os.path.isdir(kayit):
            messagebox.showerror("Eksik Bilgi", "Lütfen geçerli bir kayıt klasörü seçin.")
            return

        if not ad.lower().endswith(".pdf"):
            ad += ".pdf"

        cikis_yolu = os.path.join(kayit, ad)
        self.olusturulan_pdf = cikis_yolu

        # UI Durumu
        self._log_temizle()
        self.calisiyor = True
        self.btn_islem.configure(state="disabled", text="⏳  PDF Birleştiriliyor, Lütfen Bekleyin…", fg_color="#334155")
        self.btn_ac_pdf.configure(state="disabled")
        self.btn_ac_klasor.configure(state="disabled")
        self.prog_bar.set(0)

        t = threading.Thread(target=self._isle, args=(kaynak, cikis_yolu), daemon=True)
        t.start()

    def _isle(self, kaynak, cikis):
        tmp_dir = tempfile.mkdtemp()
        try:
            cikis_abs = os.path.abspath(cikis)
            dosyalar = sorted([
                f for f in os.listdir(kaynak)
                if os.path.splitext(f)[1].lower() in DESTEKLI_UZANTILAR
                and os.path.abspath(os.path.join(kaynak, f)) != cikis_abs
            ], key=natural_sort_key)

            if not dosyalar:
                self.after(0, messagebox.showerror, "Dosya Bulunamadı",
                           "Seçilen klasörde birleştirilecek görüntü veya PDF dosyası bulunamadı.")
                return

            toplam = len(dosyalar)
            self.after(0, self._log, f"📂 İşlem başlatıldı: {kaynak}")
            self.after(0, self._log, f"📋 Toplam {toplam} dosya sıraya alındı.\n")

            yatay = "Yatay" in self.yon.get()
            kalite = self.kalite.get()
            writer = PdfWriter()
            toplam_sayfa = 0

            yon_harf = "L" if yatay else "P"
            PW = 297 if yatay else 210
            PH = 210 if yatay else 297

            for i, f in enumerate(dosyalar, 1):
                yol = os.path.join(kaynak, f)
                ext = os.path.splitext(f)[1].lower()

                try:
                    if ext == ".pdf":
                        reader = PdfReader(yol)
                        sayfa_sayisi = len(reader.pages)
                        writer.append(yol)
                        toplam_sayfa += sayfa_sayisi
                        self.after(0, self._log, f"  📄 [{i}/{toplam}] PDF Eklendi: {f} ({sayfa_sayisi} sayfa)")
                    else:
                        img = Image.open(yol).convert("RGB")
                        w, h = img.size

                        if yatay and h > w:
                            img = img.rotate(90, expand=True)
                            w, h = img.size
                        elif not yatay and w > h:
                            img = img.rotate(90, expand=True)
                            w, h = img.size

                        tmp_jpg = os.path.join(tmp_dir, f"img_{i:04d}.jpg")
                        img.save(tmp_jpg, "JPEG", quality=kalite)

                        pdf = FPDF(orientation=yon_harf, unit="mm", format="A4")
                        pdf.add_page()
                        margin = 5
                        avail_w = PW - 2 * margin
                        avail_h = PH - 2 * margin
                        dpi = 96
                        img_w_mm = w * 25.4 / dpi
                        img_h_mm = h * 25.4 / dpi
                        ratio = min(avail_w / img_w_mm, avail_h / img_h_mm, 1.0)
                        nw = img_w_mm * ratio
                        nh = img_h_mm * ratio
                        x = (PW - nw) / 2
                        y = (PH - nh) / 2
                        pdf.image(tmp_jpg, x=x, y=y, w=nw, h=nh)

                        tmp_pdf = os.path.join(tmp_dir, f"page_{i:04d}.pdf")
                        pdf.output(tmp_pdf)

                        writer.append(tmp_pdf)
                        toplam_sayfa += 1
                        self.after(0, self._log, f"  🖼 [{i}/{toplam}] Görsel İşlendi: {f}")

                    ilerleme = i / toplam
                    self.after(0, lambda v=ilerleme: self.prog_bar.set(v))
                    self.after(0, lambda idx=i, tot=toplam, ad=f: self.lbl_durum.configure(
                        text=f"İşleniyor: {idx}/{tot} — {ad}"
                    ))
                except Exception as e:
                    self.after(0, self._log, f"  ✖ HATA / ATLANDI ({f}): {e}")

            if toplam_sayfa == 0:
                self.after(0, messagebox.showerror, "Hata", "Hiçbir sayfa birleştirilemedi.")
                return

            self.after(0, self._log, "\n📝 Nihai PDF diske yazılıyor...")
            self.after(0, lambda: self.lbl_durum.configure(text="PDF kaydediliyor..."))

            with open(cikis, "wb") as f_out:
                writer.write(f_out)
            writer.close()

            boyut_mb = os.path.getsize(cikis) / (1024 * 1024)

            self.after(0, self._log,
                       f"\n🎉 İŞLEM BAŞARIYLA TAMAMLANDI!\n"
                       f"   📄 Dosya: {os.path.basename(cikis)}\n"
                       f"   📁 Konum: {os.path.dirname(cikis)}\n"
                       f"   📊 Toplam: {toplam_sayfa} sayfa ({toplam} dosya)\n"
                       f"   📦 Boyut: {boyut_mb:.2f} MB\n")

            self.after(0, lambda: self.prog_bar.set(1.0))
            self.after(0, lambda: self.lbl_durum.configure(
                text=f"✅ Tamamlandı — {toplam_sayfa} sayfa ({boyut_mb:.2f} MB)",
                text_color="#10b981"
            ))
            self.after(0, lambda: self.btn_ac_pdf.configure(state="normal"))
            self.after(0, lambda: self.btn_ac_klasor.configure(state="normal"))

            # Klasörü otomatik aç
            self.after(0, lambda: os.startfile(os.path.dirname(cikis)))

        except Exception as e:
            self.after(0, self._log, f"\n❌ Beklenmedik Hata: {e}")
            self.after(0, messagebox.showerror, "Hata", str(e))
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)
            self.after(0, self._bitir)

    def _bitir(self):
        self.calisiyor = False
        self.btn_islem.configure(state="normal", text="🚀  PDF Oluştur ve Birleştir", fg_color="#4f46e5")


if __name__ == "__main__":
    app = ModernPdfBirlestirici()
    app.mainloop()

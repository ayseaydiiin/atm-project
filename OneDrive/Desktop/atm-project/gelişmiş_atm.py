import tkinter as tk
from tkinter import messagebox
import datetime

class ATMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ATM GİRİŞ")
        self.root.geometry("400x300")
        self.root.config(bg="#eaf6f6")  # Arka plan rengi
        self.bakiye = 1000.0
        self.islem_gecmisi = []

        self.kullanici_adi = "ayse"
        self.sifre = "1234"

        self.giris_ekrani()

    def giris_ekrani(self):
        self._temizle()

        tk.Label(self.root, text="ATM Giriş Paneli", font=("Helvetica", 16, "bold"), bg="#eaf6f6", fg="#0a3d62").pack(pady=20)

        tk.Label(self.root, text="Kullanıcı Adı:", bg="#eaf6f6", font=("Helvetica", 11)).pack()
        self.username_entry = tk.Entry(self.root, font=("Helvetica", 11))
        self.username_entry.pack()

        tk.Label(self.root, text="Şifre:", bg="#eaf6f6", font=("Helvetica", 11)).pack()
        self.password_entry = tk.Entry(self.root, show="*", font=("Helvetica", 11))
        self.password_entry.pack()

        tk.Button(self.root, text="Giriş Yap", command=self.giris_kontrol, bg="#38ada9", fg="white",
                  font=("Helvetica", 12, "bold")).pack(pady=20)

    def giris_kontrol(self):
        kullanici = self.username_entry.get()
        sifre = self.password_entry.get()

        if kullanici == self.kullanici_adi and sifre == self.sifre:
            self.ana_ekran()
        else:
            messagebox.showerror("Hatalı Giriş", "Kullanıcı adı veya şifre yanlış!")

    def ana_ekran(self):
        self._temizle()
        self.root.title("ATM Uygulaması")
        self.root.config(bg="#fdfefe")

        tk.Label(self.root, text="ATM'ye Hoşgeldiniz!", font=("Helvetica", 14, "bold"), fg="#1e3799", bg="#fdfefe").pack(pady=20)

        self._buton("💰 Bakiye Sorgula", self.bakiye_sorgula, "#1abc9c")
        self._buton("💵 Para Yatır", self.para_yatir, "#3498db")
        self._buton("🏧 Para Çek", self.para_cek, "#e67e22")
        self._buton("📋 İşlem Geçmişi", self.gecmisi_goster, "#9b59b6")
        self._buton("🚪 Çıkış Yap", self.giris_ekrani, "#95a5a6")

    def _buton(self, metin, komut, renk):
        tk.Button(self.root, text=metin, width=30, height=2, command=komut,
                  bg=renk, fg="white", font=("Helvetica", 11, "bold")).pack(pady=5)

    def bakiye_sorgula(self):
        messagebox.showinfo("Bakiye Bilgisi", f"Mevcut Bakiyeniz: {self.bakiye:.2f} TL")
        self.gecmise_ekle("Bakiye Sorgulama", 0)

    def para_yatir(self):
        self.islem_penceresi("Para Yatır", self.islem_para_yatir)

    def para_cek(self):
        self.islem_penceresi("Para Çek", self.islem_para_cek)

    def islem_penceresi(self, baslik, fonksiyon):
        pencere = tk.Toplevel(self.root)
        pencere.title(baslik)
        pencere.geometry("300x180")
        pencere.config(bg="#f7f1e3")

        tk.Label(pencere, text="Miktar girin:", bg="#f7f1e3", font=("Helvetica", 11)).pack(pady=10)
        miktar_entry = tk.Entry(pencere, font=("Helvetica", 11))
        miktar_entry.pack()

        def onayla():
            try:
                miktar = float(miktar_entry.get())
                if miktar <= 0:
                    raise ValueError
                fonksiyon(miktar)
                pencere.destroy()
            except ValueError:
                messagebox.showerror("Hata", "Geçerli bir miktar girin.")

        tk.Button(pencere, text="Onayla", command=onayla,
                  bg="#2ecc71", fg="white", font=("Helvetica", 11, "bold")).pack(pady=10)

    def islem_para_yatir(self, miktar):
        self.bakiye += miktar
        messagebox.showinfo("Başarılı", f"{miktar:.2f} TL yatırıldı.")
        self.gecmise_ekle("Para Yatırma", miktar)

    def islem_para_cek(self, miktar):
        if miktar > self.bakiye:
            messagebox.showerror("Hata", "Yetersiz bakiye!")
        else:
            self.bakiye -= miktar
            messagebox.showinfo("Başarılı", f"{miktar:.2f} TL çekildi.")
            self.gecmise_ekle("Para Çekme", miktar)

    def gecmise_ekle(self, islem, miktar):
        zaman = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.islem_gecmisi.append(f"[{zaman}] {islem} - {miktar:.2f} TL")

    def gecmisi_goster(self):
        pencere = tk.Toplevel(self.root)
        pencere.title("İşlem Geçmişi")
        pencere.geometry("400x300")
        pencere.config(bg="#dff9fb")

        tk.Label(pencere, text="İŞLEM GEÇMİŞİ", font=("Helvetica", 12, "bold"), bg="#dff9fb", fg="#130f40").pack(pady=10)
        liste = tk.Listbox(pencere, width=50, height=15, font=("Courier New", 10))
        liste.pack()

        if not self.islem_gecmisi:
            liste.insert(tk.END, "Henüz bir işlem yapılmadı.")
        else:
            for kayit in self.islem_gecmisi:
                liste.insert(tk.END, kayit)

    def _temizle(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Uygulama başlat
if __name__ == "__main__":
    root = tk.Tk()
    app = ATMApp(root)
    root.mainloop()

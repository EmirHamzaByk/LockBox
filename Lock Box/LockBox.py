import os
import tkinter as tk
from tkinter import messagebox
import sqlite3

class Sifre:
    def __init__(self):
        self.dizin = "C:/LockBox/Data/"
        os.makedirs(self.dizin, exist_ok=True)

        self.db_dosya = os.path.join(self.dizin, "Box.db")
        self.baglanti = sqlite3.connect(self.db_dosya)
        self.cursor = self.baglanti.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS sifre(id INTEGER PRIMARY KEY AUTOINCREMENT, site varchar(80), kullanici varchar(255), sifre varchar(255))")

        self.ana = tk.Tk()
        self.ana.geometry("475x475")
        self.ana.resizable(width=False, height=False)
        self.ana.title("LockBox")
        self.ana.configure(bg="#2A303C")

        self.bolge1 = tk.Frame(self.ana, padx=15, pady=15, relief="ridge", bg="#2A303C")
        self.bolge1.pack(side="top", anchor="center")

        self.site_lbl = tk.Label(self.bolge1, text="Web Sitesi:", font="Calibri", fg="#d3cfe1", bg="#2A303C")
        self.site_lbl.grid(row=0, column=0, sticky="e")
        self.site_ent = tk.Entry(self.bolge1, font="Calibri", width=30)
        self.site_ent.grid(row=0, column=1, pady=5)

        self.kullanici_lbl = tk.Label(self.bolge1, text="Kullanıcı Adı:", font="Calibri", fg="#d3cfe1", bg="#2A303C")
        self.kullanici_lbl.grid(row=1, column=0, sticky="e")
        self.kullanici_ent = tk.Entry(self.bolge1, font="Calibri", width=30)
        self.kullanici_ent.grid(row=1, column=1, pady=5)

        self.sifre_lbl = tk.Label(self.bolge1, text="Şifre:", font="Calibri", fg="#d3cfe1" ,bg="#2A303C")
        self.sifre_lbl.grid(row=2, column=0, sticky="e")
        self.sifre_ent = tk.Entry(self.bolge1, font="Calibri", width=30, show='*')
        self.sifre_ent.grid(row=2, column=1, pady=5)

        self.goz_btn = tk.Button(self.bolge1, text="Göster/Gizle", font="Verdana 10 bold", command=self.goz_simge_toggle, width=25, height=1, bg='#2A303C', fg='#FF6363', bd=0)
        self.goz_btn.grid(row=3, column=0, columnspan=2, pady=10)

        self.kaydet = tk.Button(self.bolge1, text="Kaydet", font="Verdana 10 bold", command=self.kaydet_sifre, width=25, height=3, bg='#7dc1d9', fg='#ffffff', bd=0)
        self.kaydet.grid(row=4, column=0, columnspan=2, pady=10)

        self.liste_button = tk.Button(self.ana, text="Kaydedilmiş Şifreleri Göster", anchor="center", border=1, relief="raised", fg="#326B85", command=self.liste)
        self.liste_button.pack(side="bottom", fill="x")

        self.sifre_gozlu = False

    def goz_simge_toggle(self):
        if self.sifre_gozlu:
            self.sifre_ent.config(show="*")
            self.sifre_gozlu = False
        else:
            self.sifre_ent.config(show="")
            self.sifre_gozlu = True

    def kaydet_sifre(self):
        site = self.site_ent.get()
        kullanici = self.kullanici_ent.get()
        sifre = self.sifre_ent.get()

        if not site or not kullanici or not sifre:
            messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun.")
            return

        self.cursor.execute("INSERT INTO sifre (site, kullanici, sifre) VALUES (?, ?, ?)", (site, kullanici, sifre))
        self.baglanti.commit()
        messagebox.showinfo("Başarılı", "Şifre başarıyla kaydedildi.")

        self.site_ent.delete(0, "end")
        self.kullanici_ent.delete(0, "end")
        self.sifre_ent.delete(0, "end")

    def liste(self):
        liste_ekrani = tk.Toplevel(self.ana)
        liste_ekrani.geometry("865x550")
        liste_ekrani.resizable(width=False, height=False)
        liste_ekrani.title("LockBox |DATA|")

        main_frame = tk.Frame(liste_ekrani)
        main_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(main_frame)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar_y = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollbar_y.pack(side="right", fill="y")

        scrollbar_x = tk.Scrollbar(liste_ekrani, orient="horizontal", command=canvas.xview)
        scrollbar_x.pack(side="bottom", fill="x")

        self.liste_bolge = tk.Frame(canvas, padx=15, pady=15, relief="ridge")
        self.liste_bolge.pack(side="top", anchor="center")

        self.liste_bolge.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.liste_bolge, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        self.cursor.execute("SELECT * FROM sifre")
        veriler = self.cursor.fetchall()

        for i, veri in enumerate(veriler):
            site_lbl = tk.Label(self.liste_bolge, text="Web Sitesi:", font="Calibri")
            site_lbl.grid(row=i, column=0, sticky="e")
            site_ent = tk.Entry(self.liste_bolge, font="Calibri")
            site_ent.insert(tk.END, veri[1])
            site_ent.grid(row=i, column=1)

            kullanici_lbl = tk.Label(self.liste_bolge, text="Kullanıcı Adı:", font="Calibri")
            kullanici_lbl.grid(row=i, column=2, sticky="e")
            kullanici_ent = tk.Entry(self.liste_bolge, font="Calibri")
            kullanici_ent.insert(tk.END, veri[2])
            kullanici_ent.grid(row=i, column=3)

            sifre_lbl = tk.Label(self.liste_bolge, text="Şifre:", font="Calibri")
            sifre_lbl.grid(row=i, column=4, sticky="e")
            sifre_ent = tk.Entry(self.liste_bolge, font="Calibri")
            sifre_ent.insert(tk.END, veri[3])
            sifre_ent.grid(row=i, column=5)

            guncelle_btn = tk.Button(self.liste_bolge, text="Güncelle", font="Verdana 10 bold",
                                 command=lambda row=i: self.sifre_guncelle(row), width=8, height=1,
                                 bg='#84B9CC', fg='#ffffff', bd=0)
            guncelle_btn.grid(row=i, column=6)

            sil_btn = tk.Button(self.liste_bolge, text="Sil", font="Verdana 10 bold",
                                command=lambda row=i: self.sifre_sil(row), width=5, height=1,
                                bg='#FF6363', fg='#ffffff', bd=0)
            sil_btn.grid(row=i, column=7)

        liste_ekrani.mainloop()



    def sifre_guncelle(self, row):
        liste_ekrani = self.liste_bolge.winfo_toplevel()
        liste_ekrani.destroy()

        guncelleme_ekrani = tk.Toplevel(self.ana)
        guncelleme_ekrani.geometry("360x200")
        guncelleme_ekrani.resizable(width=False, height=False)
        guncelleme_ekrani.title("LockBox |DÜZENLEME|")

        self.guncelleme_bolge = tk.Frame(guncelleme_ekrani, padx=15, pady=15, relief="ridge", bg="#2A303C")
        self.guncelleme_bolge.pack(side="top", anchor="center")

        veri = self.cursor.execute("SELECT * FROM sifre").fetchall()[row]

        site_lbl = tk.Label(self.guncelleme_bolge, text="Web Sitesi:", font="Calibri", fg="#d3cfe1",bg="#2A303C")
        site_lbl.grid(row=0, column=0, sticky="e")
        self.site_guncelle_ent = tk.Entry(self.guncelleme_bolge, font="Calibri", width=30)
        self.site_guncelle_ent.grid(row=0, column=1, pady=5)
        self.site_guncelle_ent.insert(0, veri[1])

        kullanici_lbl = tk.Label(self.guncelleme_bolge, text="Kullanıcı Adı:", font="Calibri", fg="#d3cfe1", bg="#2A303C")
        kullanici_lbl.grid(row=1, column=0, sticky="e")
        self.kullanici_guncelle_ent = tk.Entry(self.guncelleme_bolge, font="Calibri", width=30)
        self.kullanici_guncelle_ent.grid(row=1, column=1, pady=5)
        self.kullanici_guncelle_ent.insert(0, veri[2])

        sifre_lbl = tk.Label(self.guncelleme_bolge, text="Şifre:", font="Calibri", fg="#d3cfe1", bg="#2A303C")
        sifre_lbl.grid(row=2, column=0, sticky="e")
        self.sifre_guncelle_ent = tk.Entry(self.guncelleme_bolge, font="Calibri", width=30, show='')
        self.sifre_guncelle_ent.grid(row=2, column=1, pady=5)
        self.sifre_guncelle_ent.insert(0, veri[3])

        guncelle_btn = tk.Button(self.guncelleme_bolge, text="Güncelle", font="Verdana 10 bold", command=lambda: self.veritabani_guncelle(row), width=25, height=3, bg='#84B9CC', fg='#ffffff', bd=0)
        guncelle_btn.grid(row=3, column=0, columnspan=2, pady=10)

    def veritabani_guncelle(self, row):
        site = self.site_guncelle_ent.get()
        kullanici = self.kullanici_guncelle_ent.get()
        sifre = self.sifre_guncelle_ent.get()
    
        if not site or not kullanici or not sifre:
            messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun.")
            return
        
        selected_id = self.cursor.execute("SELECT id FROM sifre LIMIT 1 OFFSET ?", (row,)).fetchone()[0]
        self.cursor.execute("UPDATE sifre SET site=?, kullanici=?, sifre=? WHERE id=?", (site, kullanici, sifre, selected_id))
        self.baglanti.commit()
        messagebox.showinfo("Başarılı", "Şifre başarıyla güncellendi.")

        guncelleme_ekrani = self.guncelleme_bolge.winfo_toplevel()
        guncelleme_ekrani.destroy()


    def sifre_sil(self, row):
        liste_ekrani = self.liste_bolge.winfo_toplevel()
        liste_ekrani.destroy()

        silme_onay = messagebox.askyesno("Silme Onayı", "Bu şifreyi silmek istediğinize emin misiniz?")
        if silme_onay:
            selected_id = self.cursor.execute("SELECT id FROM sifre LIMIT 1 OFFSET ?", (row,)).fetchone()[0]
            self.cursor.execute("DELETE FROM sifre WHERE id=?", (selected_id,))
            self.baglanti.commit()
            messagebox.showinfo("Başarılı", "Şifre başarıyla silindi.")


    def baslat(self):
        self.ana.mainloop()

sifre_uygulamasi = Sifre()
sifre_uygulamasi.baslat()

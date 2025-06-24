from flask import Flask, render_template, request, redirect, session, jsonify, url_for, flash
import sqlite3
import bcrypt
from datetime import datetime

app = Flask(__name__)
app.secret_key = "cok_gizli_anahtar"

# Veritabanı oluşturma
def veritabani_olustur():
    conn = sqlite3.connect("zaman.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kullanicilar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kullanici_adi TEXT NOT NULL UNIQUE,
            sifre TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kayitlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kullanici_id INTEGER,
            sure INTEGER,
            tarih TEXT,
            FOREIGN KEY (kullanici_id) REFERENCES kullanicilar(id)
        )
    """)

    conn.commit()
    conn.close()

veritabani_olustur()

# Giriş Sayfası
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        kullanici_adi = request.form["kullanici_adi"]
        sifre = request.form["sifre"]

        conn = sqlite3.connect("zaman.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM kullanicilar WHERE kullanici_adi = ?", (kullanici_adi,))
        kullanici = cursor.fetchone()
        conn.close()

        if kullanici:
            if bcrypt.checkpw(sifre.encode("utf-8"), kullanici[2].encode("utf-8")):
                session["kullanici_id"] = kullanici[0]
                session["kullanici_adi"] = kullanici[1]
                return redirect("/zaman")
            else:
                flash("❌ Hatalı kullanıcı adı veya şifre!")
        else:
            flash("❌ Böyle bir kullanıcı bulunamadı!")

    return render_template("login.html")

# Kayıt Sayfası
@app.route("/kayit", methods=["GET", "POST"])
def kayit():
    if request.method == "POST":
        kullanici_adi = request.form["kullanici_adi"]
        sifre = request.form["sifre"]
        sifre_hash = bcrypt.hashpw(sifre.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        try:
            conn = sqlite3.connect("zaman.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO kullanicilar (kullanici_adi, sifre) VALUES (?, ?)",
                           (kullanici_adi, sifre_hash))
            conn.commit()
            conn.close()
            return redirect("/")
        except:
            flash("⚠️ Bu kullanıcı adı zaten kayıtlı!")
            return redirect("/kayit")

    return render_template("register.html")

# Zaman Sayacı Sayfası
@app.route("/zaman")
def zaman_sayaci():
    if "kullanici_id" not in session:
        return redirect("/")
    return render_template("index.html", kullanici_adi=session["kullanici_adi"])

# Sayaç Verisi Kaydetme
@app.route("/kaydet", methods=["POST"])
def kaydet():
    if "kullanici_id" not in session:
        return jsonify({"hata": "Giriş gerekli"}), 401

    veri = request.get_json()
    sure = veri.get("sure")
    tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    kullanici_id = session["kullanici_id"]

    conn = sqlite3.connect("zaman.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO kayitlar (kullanici_id, sure, tarih) VALUES (?, ?, ?)",
                   (kullanici_id, sure, tarih))
    conn.commit()
    conn.close()

    return jsonify({"durum": "kaydedildi", "sure": sure})

# Geçmiş Sayfası
@app.route("/gecmis")
def gecmis():
    if "kullanici_id" not in session:
        return redirect("/")
    conn = sqlite3.connect("zaman.db")
    cursor = conn.cursor()
    cursor.execute("SELECT sure, tarih FROM kayitlar WHERE kullanici_id = ? ORDER BY id DESC",
                   (session["kullanici_id"],))
    veriler = cursor.fetchall()
    conn.close()
    return render_template("gecmis.html", veriler=veriler)

# Çıkış
@app.route("/cikis")
def cikis():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

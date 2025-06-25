# ⏱️ Zaman Sayacı Web Uygulaması

Bu proje, kullanıcıların günlük çalışma sürelerini takip edebilecekleri, modern ve şık tasarıma sahip bir zaman takip sistemidir. Flask ile geliştirilmiş, SQLite veritabanı kullanılmıştır.

## 🚀 Özellikler

- 👤 Kullanıcı girişi ve kayıt sistemi (şifreler hashlenmiş şekilde saklanır)
- ⏳ Başlat / Durdur / Sıfırla fonksiyonlu zaman sayacı
- 🧠 Rastgele motivasyon sözleri
- 🔔 Sayacın çalıştığını belirten ses efekti
- 🌓 Karanlık / Aydınlık tema geçişi
- 📈 Geçmiş süre kayıtları
- 💾 Veritabanına süre kaydetme

## 🛠️ Kullanılan Teknolojiler

- Python (Flask)
- SQLite
- HTML5, CSS3, JavaScript
- Bootstrap (isteğe bağlı)
- bcrypt

## 📷 Ekran Görüntüsü

![Zaman Sayacı](static/screenshot.png)

## ⚙️ Kurulum

```bash
git clone https://github.com/onur0721/zaman_sayaci.git
cd zaman_sayaci
python3 -m venv venv
source venv/bin/activate  # Windows için: venv\Scripts\activate
pip install -r requirements.txt
python app.py

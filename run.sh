#!/bin/bash

echo "[*] Menghentikan server Flask lama (jika ada)..."
pkill -f "python3 app.py"

echo "[*] Menjalankan Flask app (port 7979)..."
nohup python3 app.py > flask.log 2>&1 &

sleep 3

echo "[*] Membuat tunnel publik via localhos.run (tanpa SSH key)..."
ssh -o StrictHostKeyChecking=no -R 80:localhost:7979 nokey@localhost.run

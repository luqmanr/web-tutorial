"""
# kala mau deactivate dulu
python3 -m venv env
source env/bin/activate
python3 -m pip install requests
"""
import requests

url = "https://google.com"
response = requests.get(url)

if response.status_code == 200:
    print("Berhasil mengambil halaman!")
    print(response.text[:500]) # Cetak 500 karakter pertama
else:
    print(f"Gagal mengambil halaman. Status code: {response.status_code}")

import requests
from bs4 import BeautifulSoup

# URL target
url = "http://quotes.toscrape.com/"

# --- Modul 1: Menggunakan requests untuk mengambil halaman ---
print("--- Modul 1: Menggunakan requests ---")
response = requests.get(url)

if response.status_code == 200:
    print("Berhasil mengambil halaman!")
    # Cetak 500 karakter pertama dari konten HTML
    print("Konten HTML (500 karakter pertama):")
    print(response.text[:500])
else:
    print(f"Gagal mengambil halaman. Status code: {response.status_code}")
    exit() # Keluar jika gagal mengambil halaman

print("\n" + "="*50 + "\n")

# --- Modul 2: Menggunakan Beautiful Soup untuk parsing dan ekstraksi ---
print("--- Modul 2: Menggunakan Beautiful Soup ---")

# Inisialisasi Beautiful Soup
soup = BeautifulSoup(response.text, 'html.parser')

print("Mengekstrak kutipan dan penulis:")
# Temukan semua div dengan class "quote"
quotes = soup.find_all('div', class_='quote')

for i, quote in enumerate(quotes):
    try:
        # Mengekstrak teks kutipan
        text_element = quote.find('span', class_='text')
        text = text_element.text if text_element else "Teks tidak ditemukan"

        # Mengekstrak penulis
        author_element = quote.find('small', class_='author')
        author = author_element.text if author_element else "Penulis tidak ditemukan"

        print(f"Kutipan {i+1}: {text}")
        print(f"Penulis: {author}")
        print("---")
    except Exception as e:
        print(f"Error saat mengekstrak kutipan {i+1}: {e}")
        print("---")

print("\n" + "="*50 + "\n")

print("--- Modul 3: Perbandingan (konseptual, lihat README untuk detail) ---")
print("Selesai. Untuk detail perbandingan dengan Selenium, lihat file README.")

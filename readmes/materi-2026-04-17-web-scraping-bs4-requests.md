# Web Scraping Lanjutan: Requests dan Beautiful Soup

## Pendahuluan
Sesi ini akan membahas dua pustaka Python yang sangat populer untuk web scraping: `requests` untuk membuat permintaan HTTP dan `Beautiful Soup` untuk mem-parsing HTML. Kedua pustaka ini adalah kombinasi yang kuat untuk mengekstrak data dari halaman web yang sebagian besar statis atau tidak memerlukan interaksi JavaScript yang kompleks.

**Durasi:** 2 Jam

## Prasyarat
*   Pemahaman dasar tentang HTML dan CSS.
*   Pemahaman dasar tentang Python.
*   (Opsional) Pengalaman sebelumnya dengan Selenium untuk web scraping.

## Tujuan Pembelajaran
Setelah sesi ini, Anda diharapkan dapat:
1.  Membuat permintaan HTTP (GET, POST) menggunakan pustaka `requests`.
2.  Memahami dan mengelola objek respons dari `requests` (status code, headers, body).
3.  Mem-parse dokumen HTML menggunakan `Beautiful Soup`.
4.  Menavigasi struktur HTML dan menemukan elemen berdasarkan tag, atribut, dan CSS selector.
5.  Mengekstrak teks dan atribut dari elemen HTML.
6.  Membedakan kapan harus menggunakan `requests` dan `Beautiful Soup` dibandingkan dengan Selenium.

---

## Modul 1: Memahami Permintaan HTTP dengan `requests` (± 45 menit)

### 1.1 Pengenalan `requests`
*   `requests` adalah pustaka HTTP untuk Python yang mudah digunakan.
*   Mengapa `requests`? Lebih sederhana untuk permintaan HTTP murni dibandingkan `urllib`.

### 1.2 Membuat Permintaan GET
*   Sintaks dasar: `response = requests.get(url)`
*   Objek `Response`:
    *   `response.status_code`: Memeriksa kode status HTTP (200 OK, 404 Not Found, dll.).
    *   `response.headers`: Melihat header respons.
    *   `response.text`: Mengambil konten respons dalam bentuk teks (untuk HTML, XML, JSON).
    *   `response.content`: Mengambil konten respons dalam bentuk byte (untuk gambar, file biner).
    *   `response.json()`: Menguraikan respons JSON menjadi objek Python (dictionary/list).

### 1.3 Membuat Permintaan POST (Ringkasan)
*   Sintaks dasar: `response = requests.post(url, data=payload, headers=headers)`
*   Kapan digunakan: Mengirim data ke server (misalnya, form submission).

### 1.4 Contoh Kode: Mengambil Halaman HTML
```python
import requests

url = "http://quotes.toscrape.com/"
response = requests.get(url)

if response.status_code == 200:
    print("Berhasil mengambil halaman!")
    # print(response.text[:500]) # Cetak 500 karakter pertama
else:
    print(f"Gagal mengambil halaman. Status code: {response.status_code}")
```

---

## Modul 2: Parsing HTML dengan `Beautiful Soup` (± 60 menit)

### 2.1 Pengenalan `Beautiful Soup`
*   `Beautiful Soup` adalah pustaka Python untuk mengekstrak data dari file HTML dan XML.
*   Mengapa `Beautiful Soup`? Membuat parsing HTML menjadi mudah dan intuitif.

### 2.2 Inisialisasi `Beautiful Soup`
*   Sintaks dasar: `soup = BeautifulSoup(html_doc, 'html.parser')`
*   `html_doc` bisa berupa string HTML atau file handle.
*   `'html.parser'` adalah parser standar Python. Parser lain: `lxml`, `html5lib`.

### 2.3 Menavigasi Struktur HTML (Parse Tree)
*   Objek `Tag`: Merepresentasikan tag HTML (misalnya, `<h1>`, `<p>`, `<a>`).
*   Objek `NavigableString`: Merepresentasikan teks di dalam tag.
*   Mengakses elemen langsung: `soup.title`, `soup.p`.

### 2.4 Mencari Elemen HTML
*   `soup.find(name, attrs, recursive, string, **kwargs)`: Mencari elemen pertama yang cocok.
*   `soup.find_all(name, attrs, recursive, string, limit, **kwargs)`: Mencari semua elemen yang cocok.
    *   `name`: Nama tag (misalnya, `'a'`, `'div'`).
    *   `attrs`: Atribut tag sebagai dictionary (misalnya, `{'class': 'text'}`).
    *   `class_`: Cara khusus untuk mencari atribut `class` (karena `class` adalah kata kunci Python).
*   Mengambil teks: `element.get_text()` atau `element.text`.
*   Mengambil atribut: `element['attribute_name']`.

### 2.5 Menggunakan CSS Selectors dengan `select()`
*   `soup.select(selector)`: Mencari semua elemen yang cocok dengan CSS selector.
*   `soup.select_one(selector)`: Mencari elemen pertama yang cocok dengan CSS selector.
*   Keuntungan: Seringkali lebih ringkas dan kuat untuk pencarian kompleks.

### 2.6 Contoh Kode: Mengekstrak Kutipan dari `quotes.toscrape.com`
```python
import requests
from bs4 import BeautifulSoup

url = "http://quotes.toscrape.com/"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Temukan semua div dengan class "quote"
    quotes = soup.find_all('div', class_='quote')

    for quote in quotes:
        text = quote.find('span', class_='text').text
        author = quote.find('small', class_='author').text
        print(f"Kutipan: {text}\nPenulis: {author}\n---")
else:
    print(f"Gagal mengambil halaman. Status code: {response.status_code}")
```

---

## Modul 3: Perbandingan `requests`/`Beautiful Soup` vs. Selenium (± 15 menit)

*   **`requests` + `Beautiful Soup`**:
    *   Cepat dan efisien untuk situs web statis.
    *   Tidak memuat JavaScript.
    *   Tidak memerlukan browser atau WebDriver.
    *   Cocok untuk data yang langsung ada di HTML.
*   **Selenium**:
    *   Dapat berinteraksi dengan JavaScript.
    *   Mengotomatiskan browser secara penuh.
    *   Lebih lambat dan membutuhkan sumber daya lebih besar.
    *   Cocok untuk situs web dinamis, pengujian, dan interaksi kompleks (klik tombol, isi form, scroll).

**Kapan menggunakan yang mana?**
*   **`requests` + `Beautiful Soup`**: Ketika data yang Anda butuhkan ada di sumber HTML yang dikembalikan oleh server.
*   **Selenium**: Ketika data dihasilkan oleh JavaScript atau Anda perlu mensimulasikan interaksi pengguna yang kompleks.

---

## Latihan (± 0 menit - Terintegrasi selama sesi)

*   Coba scraping di situs web lain yang sederhana (misalnya, halaman berita, blog).
*   Eksplorasi lebih lanjut dengan CSS selectors.

---

## Tanya Jawab & Diskusi (± 0 menit - Terintegrasi selama sesi)

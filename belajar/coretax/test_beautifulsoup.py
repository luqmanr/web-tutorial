"""
python3 -m pip install beautifulsoup4
"""
import requests
from bs4 import BeautifulSoup

url = "http://quotes.toscrape.com"
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

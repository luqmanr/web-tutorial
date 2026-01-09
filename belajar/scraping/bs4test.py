import requests
from bs4 import BeautifulSoup

reached_page_end = False
i = 10
while not reached_page_end:
    BASE_URL = "http://quotes.toscrape.com"
    url = f"{BASE_URL}/page/{i}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Temukan judul halaman
    title = soup.find('h1').text
    print(f"halaman {i} - Judul Halaman: {title}")

    # cek apakah ada kutipan di halaman ini
    all_divs = soup.find_all('div')
    for adiv in all_divs:
        if 'No quotes found!' in adiv.text:
            print('reached end of pages')
            reached_page_end = True
            break

    # Temukan semua kutipan
    quotes = soup.find_all('div', class_='quote')
    for quote in quotes:
        link = quote.find('a').attrs['href']
        text = quote.find('span', class_='text').text
        author = quote.find('small', class_='author').text
        print(f"\"{text}\" - {author}")
        print(f'link to about {author}: {BASE_URL}{link}\n')
        
    i += 1
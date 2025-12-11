from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Konfigurasi opsi Chrome
chrome_options = Options()
# Jika berjalan di Docker, Anda mungkin tidak memerlukan --headless untuk observasi melalui noVNC
# chrome_options.add_argument("--headless") # Komentar ini untuk demo visual

# Terhubung ke Selenium Grid Hub yang berjalan di Docker
driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    options=chrome_options
)

try:
    url = "http://quotes.toscrape.com/scroll" # Contoh halaman dengan konten dinamis
    driver.get(url)
    time.sleep(3) # Beri waktu halaman untuk memuat

    # Contoh: Gulir ke bawah untuk memuat lebih banyak konten
    last_height = driver.execute_script("return document.body.scrollHeight") # 1080
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight") # 1080 + 1080 = 2160
        if new_height == last_height:
            break
        last_height = new_height

    # Ekstrak data menggunakan BeautifulSoup setelah konten dinamis dimuat
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')

    quotes = soup.find_all('div', class_='quote')
    for i, quote in enumerate(quotes):
        text = quote.find('span', class_='text').text
        author = quote.find('small', class_='author').text
        print(f"Kutipan {i+1}: \"{text}\" - {author}")

finally:
    driver.quit()
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Mengatur service GeckoDriver
gecko_driver_path = "/home/luqmanr/bin/geckodriver"  # Sesuaikan jalur jika perlu
service = Service(gecko_driver_path)

# Mengatur opsi Firefox (opsional)
firefox_options = Options()

# Membuat driver Firefox
driver = webdriver.Firefox(service=service, options=firefox_options)

# Buka halaman login
url = "https://the-internet.herokuapp.com/login" # Changed URL to the-internet.herokuapp.com/login
driver.get(url)

# # Menunggu elemen form login muncul
wait = WebDriverWait(driver, 10)
username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))

# Masukkan username dan password (menggunakan kredensial yang valid untuk the-internet.herokuapp.com)
username_field.send_keys("tomsmith") # Changed username
password_field.send_keys("SuperSecretPassword!") # Changed password

driver.quit()
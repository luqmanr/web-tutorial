from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Membuat driver Chrome
chrome_options = Options()
driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    options=chrome_options
)

# Buka halaman login
url = "https://the-internet.herokuapp.com/login" # Changed URL to the-internet.herokuapp.com/login
driver.get(url)

# Menunggu elemen form login muncul
wait = WebDriverWait(driver, 10)
username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))

# Masukkan username dan password (menggunakan kredensial yang valid untuk the-internet.herokuapp.com)
username_field.send_keys("tomsmith") # Changed username
password_field.send_keys("SuperSecretPassword!") # Changed password

# ### 2. Menemukan Tombol Submit dan Klik

submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
submit_button.click()

# ### 3. Memeriksa Apakah Login Berhasil atau Gagal

# Cek apakah halaman berhasil dimuat atau terdapat pesan error
try:
    # Menunggu elemen flash message yang muncul setelah login
    flash_message_element = wait.until(EC.presence_of_element_located((By.ID, "flash")))
    
    if "You logged into a secure area!" in flash_message_element.text:
        print("Login berhasil!")
        print(f"Pesan: {flash_message_element.text}")
    elif "Your username is invalid!" in flash_message_element.text or "Your password is invalid!" in flash_message_element.text:
        print("Login gagal!")
        print(f"Pesan error: {flash_message_element.text}")
    else:
        print("Login status tidak dikenali.")
        print(f"Pesan: {flash_message_element.text}")

except Exception as e:
    print("Terjadi kesalahan atau elemen flash tidak ditemukan.")
    print(f"Kesalahan: {e}")

# Tutup driver
driver.quit()
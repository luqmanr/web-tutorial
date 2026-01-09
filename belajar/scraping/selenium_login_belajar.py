from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from io import BytesIO

# Membuat driver Chrome
chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080") # Added this line
driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    options=chrome_options
)

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

# # ### 2. Menemukan Tombol Submit dan Klik

# submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
# submit_button.click()

# # ### 3. Memeriksa Apakah Login Berhasil atau Gagal

# # Cek apakah halaman berhasil dimuat atau terdapat pesan error
# # Tutup driver dan capture screenshot
# try:
#     # Tambahkan code untuk mengecek flash message dan mengambil screenshot
#     # flash_message_element = wait.until(EC.presence_of_element_located((By.ID, "flash")))
#     # flash_message_element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div")))
#     flash_message_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"flash\"]")))
#     # Tutup driver
#     if "You logged into a secure area!" in flash_message_element.text:
#         print("Login berhasil!")
#         print(f"Pesan: {flash_message_element.text}")
#         driver.save_screenshot("success.png")
#         # Menemukan dan mengklik tombol logout
#         logout_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/logout']")))
#         logout_button.click()
#         print("Berhasil logout.")
#         driver.save_screenshot("logout_success.png") # Screenshot after logout
#     elif "Your username is invalid!" in flash_message_element.text or "Your password is invalid!" in flash_message_element.text:
#         print("Login gagal!")
#         print(f"Pesan error: {flash_message_element.text}")
#         driver.save_screenshot("fail.png")
#     else:
#         print("Login status tidak dikenali.")
#         print(f"Pesan: {flash_message_element.text}")
#         driver.save_screenshot("unknown_status.png") # Optionally save for unknown status

# except Exception as e:
#     print("Terjadi kesalahan atau elemen flash tidak ditemukan.")
#     print(f"Kesalahan: {e}")
#     driver.save_screenshot("error_page.png") # Save screenshot on error

# # Tutup driver
# driver.quit()

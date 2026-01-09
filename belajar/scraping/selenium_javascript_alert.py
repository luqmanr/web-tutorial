from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=chrome_options)
driver.maximize_window()

URL = "https://the-internet.herokuapp.com/javascript_alerts"
driver.get(URL)

wait = WebDriverWait(driver, 10)
print(f"✅ Berhasil navigasi ke: {URL}\n")

def click_button_by_text(text):
    """Mencari dan mengklik tombol berdasarkan teksnya."""
    button_xpath = f"//button[text()='{text}']"
    button = wait.until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
    button.click()
    print(f"👉 Mengklik tombol: '{text}'")

try:
    click_button_by_text("Click for JS Alert")
    
    js_alert = wait.until(EC.alert_is_present())
    
    print(f"   Pesan Alert: '{js_alert.text}'")
    js_alert.accept()
    
    result = driver.find_element(By.ID, "result").text
    print(f"   Result setelah Alert: {result}\n")

except Exception as e:
    print(f"❌ Error saat menangani JS Alert: {e}")

time.sleep(1)


try:
    click_button_by_text("Click for JS Confirm")
    
    js_confirm = wait.until(EC.alert_is_present())
    
    print(f"   Pesan Confirm: '{js_confirm.text}'")
    js_confirm.dismiss()
    
    result = driver.find_element(By.ID, "result").text
    print(f"   Result setelah Confirm (Dismiss): {result}\n")

except Exception as e:
    print(f"❌ Error saat menangani JS Confirm: {e}")

time.sleep(1)

try:
    click_button_by_text("Click for JS Prompt")
    
    js_prompt = wait.until(EC.alert_is_present())
    
    text_to_enter = "Halo, ini dari Selenium!"
    
    print(f"   Pesan Prompt: '{js_prompt.text}'")
    print(f"   Mengirim teks: '{text_to_enter}'")
    
    js_prompt.send_keys(text_to_enter)
    js_prompt.accept()
    
    result = driver.find_element(By.ID, "result").text
    print(f"   Result setelah Prompt: {result}\n")

except Exception as e:
    print(f"❌ Error saat menangani JS Prompt: {e}")

finally:
    print("Mengeksekusi driver.quit()")
    time.sleep(2)
    driver.quit()
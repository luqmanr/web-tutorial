url = 'https://coretaxdjp.pajak.go.id/registration-portal/id-ID/documents'

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def run_automated_task():
    chrome_options = Options()

    # 1. Path Setup
    # user_data_path = os.path.expanduser("~/.config/google-chrome")
    # chrome_options.add_argument(f"--user-data-dir={user_data_path}")
    # chrome_options.add_argument("--profile-directory=Default")

    # 2. Stability Arguments (Crucial for existing profiles)
    chrome_options.add_argument("--disable-extensions") # Extensions often cause hangs
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.page_load_strategy = 'normal' # Ensures driver waits for page load

    # 3. Prevent detection/hangs
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    try:
        print("Initializing Chrome with profile... (Make sure all other Chrome windows are closed!)")
        time.sleep(3)
        # driver = webdriver.Chrome(options=chrome_options)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        # 4. Navigate
        print("Navigating to page...")
        driver.get(url)
        
        print("Please log in manually in the browser window...")
        
        wait = WebDriverWait(driver, 60)
        username_field = wait.until(EC.presence_of_element_located((By.ID, "Username")))
        password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))

        # 5. Wait for Login (Fixed typo here)
        wait = WebDriverWait(driver, 120)
        wait.until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/regportal-root/div/ui-coretax-one-column-layout/div/div/div/dcmshr-documents/div/div[2]/ui-grid/p-table/div/div[1]/div/span/button[1]"))
        )

        print("Login detected!")
        button_refresh = driver.find_element(By.XPATH, "/html/body/regportal-root/div/ui-coretax-one-column-layout/div/div/div/dcmshr-documents/div/div[2]/ui-grid/p-table/div/div[1]/div/span/button[1]")
        print(f"Success: {button_refresh}")

        try:
            button_refresh.click()
            print("Button refresh clicked successfully!")
        except Exception as e:
            print(f"Failed to click the refresh button: {e}")

        time.sleep(300)

        driver.find_elements(By.XPATH, "/html/body/regportal-root/div/ui-coretax-one-column-layout/div/div/div/dcmshr-documents/div/div[2]/ui-grid/p-table/div/div[2]/table/tbody/tr/td[1]/div/div[1]/span")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    run_automated_task()
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        driver = webdriver.Chrome(options=chrome_options)
        
        # 4. Navigate
        print("Navigating to page...")
        driver.get("https://the-internet.herokuapp.com/login")
        
        print("Please log in manually in the browser window...")
        
        # 5. Wait for Login (Fixed typo here)
        wait = WebDriverWait(driver, 120)
        wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "a.button.secondary.radius"))
        )

        print("Login detected!")
        flash_message = driver.find_element(By.ID, "flash").text
        print(f"Success: {flash_message}")

        time.sleep(5)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    run_automated_task()

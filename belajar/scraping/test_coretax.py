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
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException

REFRESH_BUTTON_XPATH = "/html/body/regportal-root/div/ui-coretax-one-column-layout/div/div/div/dcmshr-documents/div/div[2]/ui-grid/p-table/div/div[1]/div/span/button[1]"
DOWNLOAD_BUTTON_ID = "ActionDownloadButton"
DEBUGGER_ADDRESS = "127.0.0.1:9222"


def attach_to_existing_chrome(debugger_address=DEBUGGER_ADDRESS):
    chrome_options = Options()

    # Only set the debugger address for attaching to existing session
    chrome_options.add_experimental_option("debuggerAddress", debugger_address)

    print(f"Attaching to Chrome debugger at {debugger_address}...")
    print("Make sure Chrome was launched with --remote-debugging-port=9222.")
    try:
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    except Exception as e:
        print(f"Failed to connect to Chrome at {debugger_address}")
        print("Make sure Chrome is running with: google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-coretax")
        raise e


def is_logged_in(driver):
    try:
        driver.refresh()
        time.sleep(2)

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, REFRESH_BUTTON_XPATH))
        )
        return True
    except TimeoutException:
        return False
    except Exception as e:
        print(f"Login detection error: {e}")
        return False


def wait_until_user_logged_in(driver):
    print("\nPlease log in manually in the attached Chrome browser.")
    print("Once you have finished logging in, return here and press Enter.")
    print("If you want to quit, type 'q' and press Enter.")

    while True:
        user_input = input("Press Enter to check login status: ").strip().lower()
        if user_input == 'q':
            raise SystemExit("User requested exit before login.")

        if is_logged_in(driver):
            print("Login detected!")
            return

        print("Login not detected yet. Please complete the login process and try again.\n")


def run_automated_task():
    try:
        driver = attach_to_existing_chrome()

        print("Navigating to Coretax page...")
        driver.get(url)

        wait_until_user_logged_in(driver)

        button_refresh = driver.find_element(By.XPATH, REFRESH_BUTTON_XPATH)
        print(f"Found refresh button: {button_refresh}")

        try:
            button_refresh.click()
            print("Button refresh clicked successfully!")
        except Exception as e:
            print(f"Failed to click the refresh button: {e}")

        button_locator = (By.ID, DOWNLOAD_BUTTON_ID)

        WebDriverWait(driver, 120).until(
            EC.visibility_of_element_located(button_locator)
        )

        total_pages = 3
        for page_index in range(total_pages):
            num_buttons = len(driver.find_elements(*button_locator))
            print(f"Found {num_buttons} download buttons on page {page_index + 1}.")

            for button_index in range(num_buttons):
                try:
                    current_buttons = driver.find_elements(*button_locator)
                    button = current_buttons[button_index]

                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", button)

                    print(f"Clicked button {button_index + 1} of {num_buttons}")
                    time.sleep(3)

                except StaleElementReferenceException:
                    print("DOM refreshed, retrying current button index...")
                    time.sleep(2)
                    continue
                except Exception as e:
                    print(f"Error clicking button {button_index}: {e}")

            time.sleep(5)
            next_button = driver.find_element(By.XPATH, "/html/body/regportal-root/div/ui-coretax-one-column-layout/div/div/div/dcmshr-documents/div/div[2]/ui-grid/p-table/div/p-paginator/div/button[2]")
            next_button.click()
            time.sleep(10)

        driver.find_elements(By.XPATH, "/html/body/regportal-root/div/ui-coretax-one-column-layout/div/div/div/dcmshr-documents/div/div[2]/ui-grid/p-table/div/div[2]/table/tbody/tr/td[1]/div/div[1]/span")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'driver' in locals():
            print("Script finished. Leaving the Chrome session open.")


if __name__ == "__main__":
    run_automated_task()

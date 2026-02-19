import os
import time
import hashlib
import requests
import json
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, WebDriverException

class FullSizeImageScraper:
    """
    A multi-engine scraper that attempts to find and download original high-res images
    rather than thumbnails from Google, Bing, DuckDuckGo, and Yahoo.
    Uses MD5 hashing for deduplication and handles engine-specific failures gracefully.
    """
    
    def __init__(self, download_dir="downloads"):
        self.download_dir = download_dir
        self.seen_hashes = set()
        
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        # Configure Chrome
        chrome_options = Options()
        # Headless is commented out so you can see the browser
        # chrome_options.add_argument("--headless") 
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Stealth settings to bypass bot detection
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Standard modern user-agent
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        
        # Hide selenium presence
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        })

    def _get_image_hash(self, content):
        """Generates a unique MD5 hash for the binary content of an image."""
        return hashlib.md5(content).hexdigest()

    def _save_image(self, url, engine_name):
        """Downloads the image, checks for duplicates via hash, and saves to disk."""
        try:
            # Short timeout to avoid hanging on dead links
            response = requests.get(url, timeout=10, stream=True, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
            })
            if response.status_code == 200:
                content = response.content
                img_hash = self._get_image_hash(content)
                
                if img_hash in self.seen_hashes:
                    return False, "Duplicate Content"

                img = Image.open(BytesIO(content))
                img_type = img.format.lower()
                
                if img.size[0] < 150 or img.size[1] < 150:
                    return False, "Too small"

                filename = f"{engine_name}_{img_hash}.{img_type}"
                filepath = os.path.join(self.download_dir, filename)
                
                with open(filepath, "wb") as f:
                    f.write(content)
                
                self.seen_hashes.add(img_hash)
                return True, filename
        except Exception:
            return False, "Download error"
        return False, "Failed"

    def scrape_google(self, keyword, limit):
        """
        Refined Google Scraping:
        - Specifically avoids suggestion chips/carousels.
        - Targets the main result grid thumbnails.
        - Captures the source from the expanded 'preview' pane.
        """
        try:
            print(f"[*] Scraping Google for '{keyword}'...")
            url = f"https://www.google.com/search?q={keyword}&tbm=isch"
            self.driver.get(url)
            
            count = 0
            # Narrowed selectors to avoid chips/related searches
            # Focus on images that have the 'data-nav' or specific result classes
            thumbnail_selectors = [
                "div.islrc img.Q4LuWd", 
                "div.islrc img.rg_i", 
                "div[data-ri] img"
            ]
            
            time.sleep(3)

            while count < limit:
                thumbnails = []
                for selector in thumbnail_selectors:
                    found = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if found:
                        thumbnails = found
                        break
                
                if not thumbnails:
                    print("  [!] No valid thumbnails found in the result grid.")
                    break

                for i in range(len(thumbnails)):
                    if count >= limit: break
                    
                    try:
                        # Check if element is displayed and not a small chip
                        if not thumbnails[i].is_displayed(): continue
                        
                        # Scroll to element
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", thumbnails[i])
                        time.sleep(0.5)
                        
                        # Force click to open preview pane
                        try:
                            thumbnails[i].click()
                        except:
                            self.driver.execute_script("arguments[0].click();", thumbnails[i])
                        
                        # Wait for the preview pane (the right-side or overlay panel)
                        time.sleep(2.0)
                        
                        # Modern Google uses a side-panel. We need the image that is actually VISIBLE 
                        # and has a real HTTP source (not the base64 placeholder).
                        preview_selectors = [
                            'div.v4dQwb img[src^="http"]', # Side panel image
                            'img.sFlh5c.pT0Scc',            # Common high-res class
                            '#islsp img[src^="http"]',      # Preview pane container
                            'div.IF9_9c img[src^="http"]'   # Backup preview class
                        ]
                        
                        found_full_res = False
                        for selector in preview_selectors:
                            preview_imgs = self.driver.find_elements(By.CSS_SELECTOR, selector)
                            for img in preview_imgs:
                                src = img.get_attribute('src')
                                # Extra check: the expanded image is usually the only one with naturalWidth > thumbnail size
                                if src and src.startswith('http') and not src.startswith('data:image'):
                                    n_width = int(img.get_attribute('naturalWidth') or 0)
                                    # If naturalWidth is 0, it might still be loading, wait a bit
                                    if n_width == 0:
                                        time.sleep(1)
                                        n_width = int(img.get_attribute('naturalWidth') or 0)
                                    
                                    if n_width > 250: # Standard thumbnail is usually < 200px
                                        success, detail = self._save_image(src, "google")
                                        if success:
                                            count += 1
                                            print(f"  [+] Google Saved: {detail}")
                                            found_full_res = True
                                            break
                            if found_full_res: break
                        
                    except Exception:
                        continue

                # Scroll down to fetch more results
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
                # Check for "Show more results"
                try:
                    more_btn = self.driver.find_element(By.CSS_SELECTOR, "input.mye4qd")
                    if more_btn.is_displayed():
                        more_btn.click()
                        time.sleep(2)
                except:
                    pass
                    
        except Exception as e:
            print(f"  [!] Google search failed: {e}")

    def scrape_bing(self, keyword, limit):
        try:
            print(f"[*] Scraping Bing for '{keyword}'...")
            url = f"https://www.bing.com/images/search?q={keyword}"
            self.driver.get(url)
            
            count = 0
            while count < limit:
                items = self.driver.find_elements(By.CLASS_NAME, "iusc")
                if not items: break
                
                for item in items:
                    if count >= limit: break
                    try:
                        metadata = json.loads(item.get_attribute("m"))
                        murl = metadata.get("murl") 
                        if murl:
                            success, detail = self._save_image(murl, "bing")
                            if success:
                                count += 1
                                print(f"  [+] Bing Saved: {detail}")
                    except Exception:
                        continue
                
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
        except Exception as e:
            print(f"  [!] Bing search failed: {e}")

    def scrape_duckduckgo(self, keyword, limit):
        try:
            print(f"[*] Scraping DuckDuckGo for '{keyword}'...")
            url = f"https://duckduckgo.com/?q={keyword}&iax=images&ia=images"
            self.driver.get(url)
            time.sleep(3) 
            
            count = 0
            while count < limit:
                tiles = self.driver.find_elements(By.CLASS_NAME, "tile--img")
                if not tiles: break
                
                for tile in tiles:
                    if count >= limit: break
                    try:
                        img_link = tile.find_element(By.CLASS_NAME, "tile--img__img")
                        full_res_url = tile.get_attribute("data-id") or img_link.get_attribute("src")
                        
                        if full_res_url:
                            success, detail = self._save_image(full_res_url, "ddg")
                            if success:
                                count += 1
                                print(f"  [+] DDG Saved: {detail}")
                    except Exception:
                        continue
                
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
        except Exception as e:
            print(f"  [!] DuckDuckGo search failed: {e}")

    def scrape_yahoo(self, keyword, limit):
        try:
            print(f"[*] Scraping Yahoo for '{keyword}'...")
            url = f"https://images.search.yahoo.com/search/images?p={keyword}"
            self.driver.get(url)
            
            count = 0
            while count < limit:
                items = self.driver.find_elements(By.CSS_SELECTOR, "li.ld")
                if not items: break
                
                for item in items:
                    if count >= limit: break
                    try:
                        metadata = json.loads(item.get_attribute("data"))
                        iurl = metadata.get("iurl")
                        if iurl:
                            success, detail = self._save_image(iurl, "yahoo")
                            if success:
                                count += 1
                                print(f"  [+] Yahoo Saved: {detail}")
                    except Exception:
                        continue
                
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
        except Exception as e:
            print(f"  [!] Yahoo search failed: {e}")

    def close(self):
        self.driver.quit()

def run_scraper():
    keyword = input("Enter search keyword: ")
    try:
        limit = int(input("Enter number of images per engine: "))
    except ValueError:
        limit = 5

    scraper = FullSizeImageScraper(download_dir=f"scraped_{keyword.replace(' ', '_')}")
    
    try:
        # scraper.scrape_google(keyword, limit)
        scraper.scrape_bing(keyword, limit)
        # scraper.scrape_duckduckgo(keyword, limit)
        # scraper.scrape_yahoo(keyword, limit)
    finally:
        scraper.close()
        total_unique = len(scraper.seen_hashes)
        print(f"\n[!] Scraping complete. Total unique images saved: {total_unique}")
        print(f"[!] Check the '{scraper.download_dir}' folder.")

if __name__ == "__main__":
    run_scraper()
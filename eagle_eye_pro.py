"""
EagleEye: Professional Booklet Automation & Verification Tool
Author: Alireza
License: MIT
"""

import os
import time
import re
import logging
import cv2
import numpy as np
import pytesseract
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

# --- Professional Logging Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler("automation.log"), logging.StreamHandler()]
)

class Config:
    """Project Configuration and Constants"""
    SAVE_FOLDER = "data/scanned_booklets"
    CHROME_PROFILE = r"C:\selenium_profile"
    TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    START_RANGE = 933
    END_RANGE = 1242
    TARGET_TEXT = "Page 10"
    MAX_WAIT_SECONDS = 60
    PSM_MODE = '--psm 11'

class ImageProcessor:
    """Computer Vision utility for OCR enhancement"""
    @staticmethod
    def prepare_for_ocr(pil_image):
        # Convert PIL to OpenCV format
        cv_img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        
        # Apply Adaptive Thresholding
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                       cv2.THRESH_BINARY, 11, 2)
        # Invert for sidebar focus
        inverted = cv2.bitwise_not(thresh)
        
        return [thresh, inverted]

class EagleEyeBot:
    """Main Automation Engine"""
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = Config.TESSERACT_CMD
        if not os.path.exists(Config.SAVE_FOLDER):
            os.makedirs(Config.SAVE_FOLDER)
            
        self.driver = self._init_browser()
        self.last_saved_id = -1
        self.last_action_time = time.time()

    def _init_browser(self):
        opts = Options()
        opts.add_argument(f"user-data-dir={Config.CHROME_PROFILE}")
        opts.add_argument("--window-size=1200,1800")
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        return webdriver.Chrome(options=opts)

    def extract_booklet_id(self):
        try:
            el = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Booklet')]")
            match = re.search(r'Booklet\s+(\d+)', el.text)
            return int(match.group(1)) if match else 0
        except:
            return 0

    def process_page(self):
        screenshot_png = self.driver.get_screenshot_as_png()
        pil_img = Image.open(BytesIO(screenshot_png))
        
        variants = ImageProcessor.prepare_for_ocr(pil_img)
        combined_text = ""
        for v in variants:
            combined_text += pytesseract.image_to_string(v, config=Config.PSM_MODE)

        if Config.TARGET_TEXT in combined_text or "10 of 20" in combined_text:
            book_id = self.extract_booklet_id()
            if book_id > 0 and book_id != self.last_saved_id:
                path = os.path.join(Config.SAVE_FOLDER, f"{book_id}.png")
                pil_img.save(path)
                logging.info(f"✔ Saved Booklet {book_id}")
                self.last_saved_id = book_id
                return True
        return False

    def navigate_next(self):
        ActionChains(self.driver).key_down(Keys.SHIFT).send_keys(Keys.ARROW_RIGHT).key_up(Keys.SHIFT).perform()
        time.sleep(2.5)
        self.last_action_time = time.time()

    def start(self):
        logging.info("EagleEye Bot Active. Ready for manual trigger...")
        input("Navigate to the portal and press Enter to start...")
        
        while self.last_saved_id < Config.END_RANGE:
            elapsed = time.time() - self.last_action_time
            if elapsed > Config.MAX_WAIT_SECONDS:
                logging.warning("Timeout: Forcing navigation...")
                self.navigate_next()
                continue

            if self.process_page():
                self.navigate_next()
            else:
                logging.info(f"Scanning... Timer: {int(elapsed)}s")
                time.sleep(2)

class IntegrityChecker:
    """Post-processing verification report"""
    @staticmethod
    def generate_report():
        logging.info("Running integrity verification...")
        files = os.listdir(Config.SAVE_FOLDER)
        found = {int(re.search(r'\d+', f).group()) for f in files if re.search(r'\d+', f)}
        
        missing = [i for i in range(Config.START_RANGE, Config.END_RANGE + 1) if i not in found]
        
        print("\n" + "="*30)
        print(f"REPORT FOR RANGE {Config.START_RANGE}-{Config.END_RANGE}")
        print(f"Success: {len(found)} | Missing: {len(missing)}")
        if missing: print(f"Missing IDs: {missing}")
        print("="*30)

if __name__ == "__main__":
    bot = EagleEyeBot()
    try:
        bot.start()
    except KeyboardInterrupt:
        logging.info("Terminated by user.")
    finally:
        IntegrityChecker.generate_report()
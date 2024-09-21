from typing import Union
import time
import random
import pyautogui
import numpy as np
from PIL import Image
from io import BytesIO
import cv2
from cloudflare_bypass.cloudflare_detector import CloudFlareLogoDetector, CloudFlarePopupDetector

def click_like_human(x: int, y: int, max_value: int = 5):
    delta_x = random.randint(-max_value, max_value)
    delta_y = random.randint(-max_value, max_value)
    pyautogui.click(x=x + delta_x, y=y + delta_y)

def get_browser_ui_offset(driver):
    # Get the total window height (including browser UI like tab bar, URL box)
    total_height = driver.execute_script("return window.outerHeight;")
    
    # Get the height of the viewport (the visible part of the webpage)
    viewport_height = driver.execute_script("return window.innerHeight;")
    
    # Calculate the height of the browser UI elements (tab bar, URL bar, etc.)
    browser_ui_height = total_height - viewport_height
    
    # Print the calculated heights for debugging
    print(f"Total window height: {total_height}px")
    print(f"Viewport height: {viewport_height}px")
    print(f"Browser UI height (offset): {browser_ui_height}px")
    
    return browser_ui_height



def bypass(driver, mode: str = 'light', warmup_time: int = None, timeout: int = 20, interval: int = 1):
    if warmup_time is not None:
        time.sleep(warmup_time)

    cf_popup_detector = CloudFlarePopupDetector(mode=mode)
    cf_logo_detector = CloudFlareLogoDetector(mode=mode)

    # Capture the screenshot of the browser's visible content
    screenshot = driver.get_screenshot_as_png()
    
    # Convert the screenshot to a NumPy array for processing
    image = Image.open(BytesIO(screenshot))
    img_np = np.array(image)
    
    # Convert the image to grayscale for template matching
    img_gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

    # Get the height of the browser's UI elements (tab bar, URL box, etc.)
    BROWSER_UI_OFFSET_Y = get_browser_ui_offset(driver)

    t0 = time.time()
    clicked = False

    while cf_logo_detector.is_detected(img_gray):
        if not clicked and cf_popup_detector.is_detected(img_gray):
            # Get CAPTCHA center coordinates
            x1, y1, x2, y2 = cf_popup_detector.matched_bbox
            captcha_center_x = (x1 + x2) // 2
            captcha_center_y = (y1 + y2) // 2 + BROWSER_UI_OFFSET_Y  # Adjust Y with the browser's offset

            # Click the CAPTCHA checkbox
            click_like_human(captcha_center_x, captcha_center_y)
            clicked = True

        time.sleep(interval)

        if time.time() - t0 > timeout:
            return clicked

    return clicked

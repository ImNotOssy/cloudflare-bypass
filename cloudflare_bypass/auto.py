from typing import Union
import time
import random
import pyautogui
from cloudflare_bypass.cloudflare_detector import CloudFlareLogoDetector, CloudFlarePopupDetector


def wait_until(detector, driver, warmup_time: Union[None, int] = None, timeout: int = 20):
    if warmup_time:
        time.sleep(warmup_time)

    t0 = time.time()
    while True:
        time.sleep(1)
        if detector.is_detected(driver):
            return detector.matched_bbox

        if time.time() - t0 > timeout:
            break


def click_like_human(x: int, y: int, max_value: int = 5):
    delta_x = random.randint(-max_value, max_value)
    delta_y = random.randint(-max_value, max_value)
    pyautogui.click(x=x + delta_x, y=y + delta_y)


def bypass(
    driver,
    mode: str = 'light',
    warmup_time: int = None,
    timeout: int = 20,
    interval: int = 1,
):
    # Optionally wait for warmup_time before starting the detection process
    if warmup_time is not None and isinstance(warmup_time, (int, float)):
        time.sleep(warmup_time)

    # Initialize CloudFlare detectors with the specified mode
    cf_popup_detector = CloudFlarePopupDetector(mode=mode)
    cf_logo_detector = CloudFlareLogoDetector(mode=mode)

    t0 = time.time()
    clicked = False
    while cf_logo_detector.is_detected(driver):
        # Click on the popup if detected and not clicked before
        if not clicked and cf_popup_detector.is_detected(driver):
            x1, y1, x2, y2 = cf_popup_detector.matched_bbox
            cx = x1 + int((x2 - x1) * 0.1)
            cy = (y1 + y2) // 2
            click_like_human(x=cx, y=cy)
            clicked = True

        # Wait for `interval` second before the next iteration
        time.sleep(interval)

        # Check if the timeout has been reached
        if time.time() - t0 > timeout:
            return clicked

    return clicked

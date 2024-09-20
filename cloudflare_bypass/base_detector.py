from typing import Union, Tuple
import cv2
from PIL import Image
import numpy as np
from io import BytesIO

class BaseDetector:
    def __init__(self, template_path: str, threshold: float = 0.6) -> None:
        self.template = cv2.imread(template_path, 0)
        self.threshold = threshold
        self.matched_bbox = None

    def _match(self, img: np.ndarray, template: np.ndarray) -> Union[None, Tuple[int]]:
        result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        _, confidence, _, max_loc = cv2.minMaxLoc(result)

        if confidence >= self.threshold:
            h, w = template.shape
            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            return top_left[0], top_left[1], bottom_right[0], bottom_right[1]
        else:
            return None

    def is_detected(self, driver) -> bool:
        screenshot = driver.get_screenshot_as_png()
        image = Image.open(BytesIO(screenshot))
        img_np = np.array(image)
        img_gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

        self.matched_bbox = self._match(img_gray, self.template)
        return self.matched_bbox is not None

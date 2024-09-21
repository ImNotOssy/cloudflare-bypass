from typing import Union, Tuple
import cv2
import numpy as np

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

    def is_detected(self, screenshot: np.ndarray) -> bool:
        self.matched_bbox = self._match(screenshot, self.template)
        return self.matched_bbox is not None

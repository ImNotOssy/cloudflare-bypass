from pathlib import Path
import sys
from cloudflare_bypass.base_detector import BaseDetector

if hasattr(sys, '_MEIPASS'):
    image_dir = Path(sys._MEIPASS) / 'cloudflare_bypass' / 'images'
else:
    image_dir = Path(__file__).parent / 'images'


class CloudFlarePopupDetector(BaseDetector):
    def __init__(self, mode: str = 'light'):
        if mode == 'light':
            self.template_path = str(image_dir / 'cf_popup.png')
        else:
            self.template_path = str(image_dir / 'cf_popup_dark.png')

        super().__init__(template_path=self.template_path)


class CloudFlareLogoDetector(BaseDetector):
    def __init__(self, mode: str = 'light'):
        if mode == 'light':
            self.template_path = str(image_dir / 'cf_logo.png')
        else:
            self.template_path = str(image_dir / 'cf_logo_dark.png')
        super().__init__(template_path=self.template_path)

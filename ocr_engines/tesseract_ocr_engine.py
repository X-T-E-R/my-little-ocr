import subprocess
from ocr_engines.base_ocr_engine import BaseOCREngine, OCRItem
from typing import Callable

class TesseractOCREngine(BaseOCREngine):
    ocr_engine_name : str = "Tesseract OCR Engine"

    def __init__(self, engines_configs: dict):
        super().__init__(engines_configs)
        self.lang = engines_configs["third_party_engine_ocr_lang"]
        self.tesseract_path = engines_configs["TesseractOCR_filepath"]

    def ocr(self, img_path: str):
        command = [self.tesseract_path, img_path, "-", "-l", "+".join(self.lang)]
        proc = subprocess.run(command, capture_output=True)
        text = proc.stdout.decode("utf-8").strip()

        # Since Tesseract doesn't give positions directly, we set position and score to None
        ocr_item = OCRItem(text=text, position=None, score=None)
        return [ocr_item]

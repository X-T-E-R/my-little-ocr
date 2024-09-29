from paddleocr import PaddleOCR
from ocr_engines.base_ocr_engine import BaseOCREngine, OCRItem
from typing import Callable

class PaddleOCREngine(BaseOCREngine):
    ocr_engine_name = "PaddleOCR"

    def __init__(self, engines_configs: dict):
        super().__init__(engines_configs)
        self.paddle_ocr = PaddleOCR(
            use_angle_cls=False, lang="ch", det_limit_side_len=int(engines_configs["ocr_short_size"])
        )

    def ocr(self, img_path: str):
        result = self.paddle_ocr.ocr(img_path, cls=False)
        ocr_item_list = []
        for line in result:
            position = [[round(coord[0]), round(coord[1])] for coord in line[0]]
            text = line[1][0]
            score = line[1][1]
            ocr_item = OCRItem(text=text, position=position, score=score)
            ocr_item_list.append(ocr_item)
        return ocr_item_list

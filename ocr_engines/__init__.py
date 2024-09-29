from .base_ocr_engine import (
    BaseOCREngine,
    OCRItem,
)

from .wechat_ocr.wechat_ocr_engine import WechatOCREngine
# from .tesseract_ocr_engine import TesseractOCREngine
# from .paddle_ocr_engine import PaddleOCREngine
from src.config import ocr_settings
from typing import Callable

ocr_engine_class_map = {
    "wechat_ocr": WechatOCREngine,
    # "tesseract_ocr": TesseractOCREngine,
    # "paddle_ocr": PaddleOCREngine,
}

Undefined = object()


class OCREngineFactory:
    _instances = {}

    @staticmethod
    def init_engine(
        engine_name: str,
    ) -> BaseOCREngine:
        if engine_name not in OCREngineFactory._instances:
            Engine_Class = ocr_engine_class_map.get(engine_name)
            if Engine_Class is None:
                raise ValueError(f"Invalid engine_name '{engine_name}' provided")
            OCREngineFactory._instances[engine_name] = Engine_Class(
                **ocr_settings.engine_configs.get(engine_name, {})
            )
        return OCREngineFactory._instances[engine_name]


get_ocr_engine = OCREngineFactory.init_engine

# ocr_engine = get_ocr_engine(ocr_settings.engine)

from .wechat_ocr_modified_lib import OcrManager
from pydantic import BaseModel, Field, field_validator
from typing import Callable
from src.base_ocr_engine import (
    BaseOCREngine,
    OCRItem,
    convert_imagelike_to_type,
    ImageLike,
    OCRResult,
)
from threading import Lock
from concurrent.futures import Future
from pathlib import Path

from .install import install
install()

class WechatOCRSettings(BaseModel):
    dir: str = Field(..., description="The directory of the WeChat OCR binary")
    exe_path: str = Field(..., description="The path to the WeChat OCR executable")
    
    @field_validator("dir", "exe_path", mode="before")
    def convert_to_path(cls, v):
        return str(Path(v).resolve())


class WechatOCREngine(BaseOCREngine):
    ocr_engine_name = "WeChat OCR"

    def __init__(
        self,
        dir: str = Path(__file__).parent / "wxocr-binary",
        exe_path: str = Path(__file__).parent / "wxocr-binary" / "WeChatOCR.exe",
        *args,
        **kwargs
    ):
        self.ocr_settings = WechatOCRSettings(dir=dir, exe_path=exe_path, **kwargs)

        self.ocr_manager: OcrManager = None
        self._future_results: dict[str, Future] = {}
        self._lock = Lock()

        self.init_wechat_ocr()

    def _wrapper_callback(self, img_path: str, wechat_ocr_results: dict):
        ocr_result = wechat_ocr_results["ocrResult"]
        ocr_item_list = []
        for item_dict in ocr_result:
            location = item_dict["location"]  # dict
            left, top, right, bottom = (
                location["left"],
                location["top"],
                location["right"],
                location["bottom"],
            )
            position = [[left, top], [right, top], [right, bottom], [left, bottom]]
            score = item_dict.get("score")
            ocr_item = OCRItem(
                text=item_dict["text"], box=position, confidence=score
            )
            ocr_item_list.append(ocr_item)

        future = self._future_results.get(str(img_path))
        if future:
            future.set_result(ocr_item_list)

    def init_wechat_ocr(self):
        self.ocr_manager: OcrManager = OcrManager(self.ocr_settings.dir)
        self.ocr_manager.SetExePath(self.ocr_settings.exe_path)
        self.ocr_manager.SetUsrLibDir(self.ocr_settings.dir)
        self.ocr_manager.SetOcrResultCallback(self._wrapper_callback)
        self.ocr_manager.StartWeChatOCR()

    def ocr_image_using_callback(self, img_path: str):
        self.ocr_manager.DoOCRTask(img_path)

    def ocr(self, img: ImageLike) -> OCRResult:
        img_path = convert_imagelike_to_type(img, "filepath")
        img_path = str(Path(img_path).resolve())
        future = Future()
        with self._lock:
            self._future_results[img_path] = future

        print(f"OCR method img_path: {img_path}")  # Debug statement

        self.ocr_image_using_callback(img_path)

        result = future.result(timeout=10)

        with self._lock:
            del self._future_results[img_path]

        return OCRResult(ocr_items=result)
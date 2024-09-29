import sys
from pathlib import Path
sys.path.append(Path(__file__).resolve().parents[1].as_posix())

from ocr_engines import get_ocr_engine, OCRItem, WechatOCREngine


test_engines = ["wechat_ocr"]

for engine_name in test_engines:
    engine = get_ocr_engine(engine_name)
    test_img_path = Path(__file__).resolve().parent / "ocr_images" / "OCR_test_1080_zh-Hans-CN.png"
    result = engine.ocr(test_img_path)
    print(f"Engine: {engine_name}")
    print([item.dict() for item in result])

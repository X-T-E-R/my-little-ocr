import sys
from pathlib import Path
sys.path.append(Path(__file__).resolve().parents[1].as_posix())

from my_little_ocr import get_all_engines


for engine_name, engine in get_all_engines().items():
    print(f"Now testing {engine_name}")
    engine_instance = engine()
    result = engine_instance.ocr(r"test\ocr_images\OCR_test_1080_zh-Hans-CN.png")
    print(result.to_list())

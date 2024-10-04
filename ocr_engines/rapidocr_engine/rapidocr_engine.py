from typing import Literal
from rapidocr_onnxruntime import RapidOCR
from pathlib import Path
from src.base_ocr_engine import (
    BaseOCREngine,
    OCRItem,
    OCRResult,
    ImageLike,
    convert_imagelike_to_type,
)

RECOGNITION_MODELS = Literal[
    "ch_PP-OCRv4_rec_infer.onnx",
    "ch_PP-OCRv3_rec_infer.onnx",
    "ch_PP-OCRv2_rec_infer.onnx",
    "ch_ppocr_server_v2.0_rec_infer.onnx",
    "en_PP-OCRv3_rec_infer.onnx",
    "en_number_mobile_v2.0_rec_infer.onnx",
    # "korean_mobile_v2.0_rec_infer.onnx",
    "japan_rec_crnn_v2.onnx",
]

DETECTION_MODELS = Literal[
    "ch_PP-OCRv4_det_infer.onnx",
    "ch_PP-OCRv3_det_infer.onnx",
    "ch_PP-OCRv2_det_infer.onnx",
    "ch_ppocr_server_v2.0_det_infer.onnx",
    "en_PP-OCRv3_det_infer.onnx",
    "en_number_mobile_v2.0_det_infer.onnx",
    # "korean_mobile_v2.0_rec_infer.onnx",
    "japan_rec_crnn_v2.onnx",
]


def get_model_version_by_name(model_name: str):
    model_versions = ["PP-OCRv4", "PP-OCRv3", "PP-OCRv2", "PP-OCRv1"]
    for version in model_versions:
        if version in model_name:
            return version
    return "PP-OCRv1"


import requests
from tqdm import tqdm


def try_download_model(model_name: str) -> Path:
    if Path(model_name).exists():
        return Path(model_name)

    # https://huggingface.co/SWHL/RapidOCR/resolve/main/PP-OCRv1/ch_ppocr_mobile_v2.0_det_infer.onnx?download=true
    model_folder = get_model_version_by_name(model_name)
    model_name = model_name.split("/")[-1]
    model_url = f"https://huggingface.co/SWHL/RapidOCR/resolve/main/{model_folder}/{model_name}?download=true"
    model_path = Path(__file__).parent / "models" / model_folder / model_name
    model_path.parent.mkdir(parents=True, exist_ok=True)
    if not model_path.exists():
        response = requests.get(model_url, stream=True)
        total_size = int(response.headers.get("content-length", 0))
        block_size = 1024

        with open(model_path, "wb") as file, tqdm(
            desc=model_name,
            total=total_size,
            unit="iB",
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(block_size):
                file.write(data)
                bar.update(len(data))

    return model_path


class RapidOCREngine(BaseOCREngine):
    def __init__(
        self,
        det_model: DETECTION_MODELS = "ch_PP-OCRv4_det_infer.onnx",
        rec_model: RECOGNITION_MODELS = "ch_PP-OCRv4_rec_infer.onnx",
        **kwargs,
    ):
        self.engine = RapidOCR(
            det_model_path=try_download_model(det_model),
            rec_model_path=try_download_model(rec_model),
            **kwargs,
        )

    def ocr(self, image: ImageLike):
        img = convert_imagelike_to_type(image, type="numpy")
        _result, elapse = self.engine(img)
        result = []
        for line in _result:
            result.append(OCRItem(text=line[1], confidence=line[2], box=line[0]))
        return OCRResult(ocr_items=result)

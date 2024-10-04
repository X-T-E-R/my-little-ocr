from PIL import Image
from surya.ocr import run_ocr, TextLine, OCRResult as SuryaOCRResult
from surya.model.detection.model import (
    load_model as load_det_model,
    load_processor as load_det_processor,
)
from surya.model.recognition.model import load_model as load_rec_model
from surya.model.recognition.processor import load_processor as load_rec_processor

from iso639 import Lang
from src.base_ocr_engine import (
    BaseOCREngine,
    OCRItem,
    ImageLike,
    OCRResult,
    convert_imagelike_to_type,
)
from typing import Literal, Optional, List

# fmt: off
SURYA_LANGS = [
    "_math", "en", "zh", "ja",
    "af", "am", "ar", "as", "az", "be", "bg", "bn", "br", "bs", "ca",
    "cs", "cy", "da", "de", "el", "eo", "es", "et", "eu", "fa", "fi", "fr", 
    "fy", "ga", "gd", "gl", "gu", "ha", "he", "hi", "hr", "hu", "hy", "id", 
    "is", "it", "jv", "ka", "kk", "km", "kn", "ko", "ku", "ky", "la", "lo", 
    "lt", "lv", "mg", "mk", "ml", "mn", "mr", "ms", "my", "ne", "nl", "no", 
    "om", "or", "pa", "pl", "ps", "pt", "ro", "ru", "sa", "sd", "si", "sk", 
    "sl", "so", "sq", "sr", "su", "sv", "sw", "ta", "te", "th", "tl", "tr", 
    "ug", "uk", "ur", "uz", "vi", "xh", "yi"
] 
# fmt: on



def convert_langs_to_surya_langs(langs: list[str]) -> list[str]:
    known_langs = set(langs) & set(SURYA_LANGS)
    unknown_langs = set(langs) - set(SURYA_LANGS)
    surya_langs = [Lang(lang).pt1 for lang in unknown_langs]
    surya_langs = surya_langs + list(known_langs)
    return surya_langs


class SuryaEngine(BaseOCREngine):
    ocr_engine_name = "surya"

    def __init__(self, default_langs: list[str] = ["en", "zh", "_math"], **kwargs):
        self.default_langs = convert_langs_to_surya_langs(default_langs)
        self.det_processor, self.det_model = load_det_processor(), load_det_model()
        self.rec_model, self.rec_processor = load_rec_model(), load_rec_processor()

    def ocr(self, img: ImageLike, langs: Optional[list[str]] = None) -> list[OCRItem]:
        img = convert_imagelike_to_type(img, type="pil")
        if langs is None:
            langs = self.default_langs
        else:
            langs = convert_langs_to_surya_langs(langs)
        predictions: SuryaOCRResult = run_ocr(
            [img],
            [langs],
            self.det_model,
            self.det_processor,
            self.rec_model,
            self.rec_processor,
        )
        result = []
        assert len(predictions) > 0, "No predictions found"
        text_lines: List[TextLine] = predictions[0].text_lines
        for line in text_lines:
            result.append(
                OCRItem(
                    text=line.text, polygon=line.polygon, confidence=line.confidence
                )
            )
        return OCRResult(ocr_items=result)


from src.engine_config import EngineConfig, register_engine

engine_config = EngineConfig(
    engine_name="surya",
    engine_class=SuryaEngine,
    project_url="https://github.com/VikParuchuri/surya",
)

register_engine(engine_config)

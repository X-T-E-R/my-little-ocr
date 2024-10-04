from my_little_ocr.base_engine.base_ocr_engine import (
    BaseOCREngine,
    OCRItem,
    OCRResult,
    ImageLike,
    convert_imagelike_to_type,
)
from typing import Literal, Optional, List
import easyocr

# fmt: off
EASYOCR_LANGS = [
    'af','az','bs','cs','cy','da','de','en','es','et','fr','ga',
    'hr','hu','id','is','it','ku','la','lt','lv','mi','ms','mt',
    'nl','no','oc','pi','pl','pt','ro','rs_latin','sk','sl','sq',
    'sv','sw','tl','tr','uz','vi','ar','fa','ug','ur','bn','as','mni',
    'ru','rs_cyrillic','be','bg','uk','mn','abq','ady','kbd','ava',
    'dar','inh','che','lbe','lez','tab','tjk','hi','mr','ne','bh','mai',
    'ang','bho','mah','sck','new','gom','sa','bgc','th','ch_sim','ch_tra',
    'ja','ko','ta','te','kn'
]
# fmt: on

from iso639 import Lang


def convert_langs_to_easyocr_langs(langs: list[str]) -> list[str]:
    special_langs = ["ch_sim", "ch_tra", "rs_latin", "rs_cyrillic"]
    unknown_langs = set(langs) - set(EASYOCR_LANGS)
    known_langs = set(langs) - unknown_langs
    special_langs_in_langs = set(langs) & set(special_langs)

    pt1_to_easy_ocr = {
        "zh": "ch_sim",
        "ab": "abq",
        "ce": "che",
        "tg": "tjk",
        "sr": "rs_latin",
    }
    result = []
    result.extend(special_langs_in_langs)
    for lang in unknown_langs:
        lang_pt1 = Lang(lang).pt1
        result.append(pt1_to_easy_ocr.get(lang_pt1, lang_pt1))
    result.extend(known_langs)
    return result


class EasyOCREngine(BaseOCREngine):
    ocr_engine_name = "easyocr"
    default_langs: list[str] = ["en"]

    def __init__(self, default_langs: list[str] = ["ch_sim", "en"], **kwargs):
        self.default_langs = convert_langs_to_easyocr_langs(default_langs)
        self.reader = easyocr.Reader(lang_list=self.default_langs, **kwargs)

    def ocr(self, img: ImageLike, **kwargs) -> OCRResult:
        img = convert_imagelike_to_type(img, "numpy")
        result = self.reader.readtext(img, **kwargs)
        return OCRResult(ocr_items=[
            OCRItem(text=item[1], confidence=item[2], box=item[0])
            for item in result
        ])


from my_little_ocr.base_engine.engine_config import EngineConfig, register_engine

engine_config = EngineConfig(
    engine_name="easyocr",
    engine_class=EasyOCREngine,
    project_url="https://github.com/JaidedAI/EasyOCR",
)

register_engine(engine_config)

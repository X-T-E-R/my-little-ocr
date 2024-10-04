from src.base_ocr_engine import BaseOCREngine, OCRResult, OCRItem, ImageLike, convert_imagelike_to_type
from PIL import Image
import pytesseract
import numpy as np
from iso639 import Lang
from .install import get_tesseract_command, check_tesseract_installed

# fmt: off
TESSERACT_LANGS = [
    'afr', 'amh', 'ara', 'asm', 'aze', 'aze_cyrl', 'bel', 'ben', 'bod', 'bos', 'bul', 'cat', 'ceb', 'ces', 'chi_sim', 
    'chi_tra', 'chr', 'cym', 'dan', 'deu', 'dzo', 'ell', 'eng', 'enm', 'epo', 'est', 'eus', 'fas', 'fin', 'fra', 'frk', 
    'frm', 'gle', 'glg', 'grc', 'guj', 'hat', 'heb', 'hin', 'hrv', 'hun', 'iku', 'ind', 'isl', 'ita', 'ita_old', 'jav', 
    'jpn', 'kan', 'kat', 'kat_old', 'kaz', 'khm', 'kir', 'kor', 'kur', 'lao', 'lat', 'lav', 'lit', 'mal', 'mar', 'mkd', 
    'mlt', 'msa', 'mya', 'nep', 'nld', 'nor', 'ori', 'pan', 'pol', 'por', 'pus', 'ron', 'rus', 'san', 'sin', 'slk', 
    'slv', 'spa', 'spa_old', 'sqi', 'srp', 'srp_latn', 'swa', 'swe', 'syr', 'tam', 'tel', 'tgk', 'tgl', 'tha', 'tir', 
    'tur', 'uig', 'ukr', 'urd', 'uzb', 'uzb_cyrl', 'vie', 'yid']
# fmt: on

replace_langs = {
    "chi": "chi_sim",
}

def convert_langs_to_tesseract_langs(langs: list[str]) -> list[str]:
    known_langs = set(TESSERACT_LANGS) & set(langs)
    unknown_langs = set(langs) - set(TESSERACT_LANGS)
    result = list(known_langs)
    for lang in unknown_langs:
        lang_pt2 = Lang(lang).pt2b
        result.append(replace_langs.get(lang_pt2, lang_pt2))
    return result


class TesseractEngine(BaseOCREngine):
    def __init__(self, tesseract_command: str = None, default_langs: list[str] = ["eng", "chi_sim"]):
        self.tesseract_command = tesseract_command or get_tesseract_command()
        check_tesseract_installed(self.tesseract_command)
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_command
        self.default_langs = default_langs
        
    def ocr(self, img: ImageLike, langs: list[str] = None, commands: list[str] = None) -> OCRResult:
        pil_img = convert_imagelike_to_type(img, type="filepath")
        langs = langs or self.default_langs
        commands = commands or []
        langs = convert_langs_to_tesseract_langs(langs)
        commands.append(f"-l {'+'.join(langs)}")
        text = pytesseract.image_to_data(pil_img, output_type=pytesseract.Output.DICT, config=" ".join(commands))
        left_list, top_list, height_list, width_list, conf_list,text_list = text['left'], text['top'], text['height'], text['width'], text['conf'],text['text']
        result = []
        for left, top, height, width, conf,text in zip(left_list, top_list, height_list, width_list, conf_list,text_list):
            if conf <0:
                continue
            confidence = conf / 100
            ocr_item = OCRItem(
                text=text,
                confidence=confidence,
                polygon=[[left, top], [left + width, top], [left + width, top + height], [left, top + height]]
            )
            result.append(ocr_item)
        return OCRResult(ocr_items=result)


from src.engine_config import EngineConfig

engine_config = EngineConfig(
    engine_name="tesseract",
    engine_class=TesseractEngine,
    project_url="https://github.com/madmaze/pytesseract"
)

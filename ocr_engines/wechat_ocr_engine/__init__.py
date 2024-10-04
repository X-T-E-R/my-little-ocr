from src.engine_config import EngineConfig, register_engine
from .wechat_ocr_engine import WechatOCREngine

engine_config = EngineConfig(
    engine_name='wechat_ocr',
    engine_class=WechatOCREngine,
    project_url="https://github.com/kanadeblisst00/wechat_ocr",
)

register_engine(engine_config)

from pydantic import BaseModel, Field
from .base_ocr_engine import BaseOCREngine
from typing import Type, Dict, Any, Optional, Callable

class EngineConfig(BaseModel):
    engine_name: str
    engine_class: Type[BaseOCREngine]
    project_url: Optional[str] = None

engines: Dict[str, EngineConfig] = {}

def register_engine(engine_config: EngineConfig):
    engines[engine_config.engine_name] = engine_config

def get_engine(engine_name: str) -> EngineConfig:
    return engines[engine_name]

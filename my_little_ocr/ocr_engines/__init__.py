from src.engine_config import get_engine as get_engine_after_register
from src.base_ocr_engine import BaseOCREngine
import importlib
from typing import Type
from pathlib import Path

engine_instances :dict[str, BaseOCREngine] = {}

def deal_with_engine_name(engine_name: str) -> str:
    engine_name_with_engine = engine_name if engine_name.endswith("_engine") else engine_name + "_engine"
    engine_name = engine_name_with_engine.replace("_engine", "")
    return engine_name, engine_name_with_engine


def get_engine_class(engine_name: str) -> Type[BaseOCREngine]:
    engine_name, engine_name_with_engine = deal_with_engine_name(engine_name)
    importlib.import_module(f"ocr_engines.{engine_name_with_engine}")
    return get_engine_after_register(engine_name).engine_class

def get_engine_instance(engine_name: str) -> BaseOCREngine:
    engine_name, engine_name_with_engine = deal_with_engine_name(engine_name)
    engine_class = get_engine_class(engine_name)
    if engine_name_with_engine in engine_instances:
        return engine_instances[engine_name_with_engine]
    engine_instances[engine_name_with_engine] = engine_class()
    return engine_instances[engine_name_with_engine]

def get_all_engines():
    result: dict[str, Type[BaseOCREngine]] = {}
    for file_or_folder in Path(__file__).parent.iterdir():
        try:
            stem = file_or_folder.stem
            if stem.endswith("_engine"):
                engine_name = stem[:-7]
                engine_class = get_engine_class(engine_name)
                result[engine_name] = engine_class
        except Exception as e:
            print(f"Error: {e}")
    return result

__all__ = ["get_engine_instance", "get_all_engines",  "get_engine_class"]

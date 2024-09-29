import sys
from pathlib import Path

sys.path.append(Path(__file__).resolve().parent.as_posix())

from dynaconf import Dynaconf
from pydantic import BaseModel, Field
from typing import Optional, Literal

# setup before importing settings
from bootstrap import setup

setup()

settings = Dynaconf(
    envvar_prefix="SCREENDIARY",
    settings_files=["settings.toml", ".secrets.toml"],
    load_dotenv=True,
    merge_enabled=True,
)


class DB_Settings(BaseModel):
    host: str = Field(
        default="localhost", description="The hostname of the MongoDB server"
    )
    port: int = Field(
        default=27017, description="The port number of the MongoDB server"
    )
    username: Optional[str] = Field(
        default=None, description="The username to connect to the MongoDB server"
    )
    password: Optional[str] = Field(
        default=None, description="The password to connect to the MongoDB server"
    )


db_settings = DB_Settings(**settings.db)


class OCR_Settings(BaseModel):
    engine: Literal["wechat_ocr"] = Field(..., description="The OCR engine to use")
    engine_configs: dict[str, dict] = Field(
        ..., description="The configurations for OCR engines"
    )


ocr_settings = OCR_Settings(**settings.ocr)

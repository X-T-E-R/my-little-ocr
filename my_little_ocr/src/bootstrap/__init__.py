from . import setup_config
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

os.chdir(Path(__file__).resolve().parents[2])
logger.info(f"Changing working directory to {os.getcwd()}")

def setup():
    setup_config.setup()

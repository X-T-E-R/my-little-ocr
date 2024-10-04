from pathlib import Path
import logging
import shutil

logger = logging.getLogger(__name__)

def copy_settings_example(example_path_str: str, target_path_str: str):
    example_path = Path(example_path_str)
    target_path = Path(target_path_str)
    if target_path.exists():
        logger.info(f"{target_path} already exists, skipping")
        return
    else:
        try:
            logger.info(f"Copying {example_path} to {target_path}")
            shutil.copy(example_path, target_path)
        except Exception as e:
            logger.error(f"Failed to copy {example_path} to {target_path}")
            # Create Empty File
            target_path.touch()

def setup():
    copy_settings_example("settings.toml.example", "settings.toml")
    copy_settings_example(".secrets.toml.example", ".secrets.toml")
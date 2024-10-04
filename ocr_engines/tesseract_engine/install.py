import os
import platform
import subprocess
from pathlib import Path
import urllib.request

def get_tesseract_command():
    system = platform.system()
    if system == "Windows":
        path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        return path 
    else:
        return "tesseract"


def check_tesseract_installed(tesseract_command: str) -> bool:
    try:
        result = subprocess.run([str(tesseract_command), "--version"], check=True, capture_output=True, text=True)
        print("Tesseract installed successfully:\n", result.stdout)
    except subprocess.CalledProcessError:
        print("Tesseract installation failed.")
        return False
    except Exception as e:
        print(f"Error checking Tesseract installation: {e}")
        return False
    return True

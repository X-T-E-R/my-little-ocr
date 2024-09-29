from abc import ABC, abstractmethod
from typing import  Optional
from pydantic import BaseModel, Field, field_validator
import numpy as np
from typing import Union, Literal
from PIL import Image
from os import PathLike
from io import BytesIO
import cv2  # OpenCV
import tempfile

ImageLike = Union[str, bytes, np.ndarray, Image.Image, PathLike]

class OCRItem(BaseModel):
    """
    Represents an OCR item containing text and its location.
    """
    text: str = Field(..., description="The text content of the OCR item")
    # 4 points, each represented as a list of 2 integers
    position: Optional[list[list[int]]] = Field(None, description="The position of the OCR item in the image, represented as a list of 4 points")
    score: Optional[float] = Field(None, description="The confidence score of the OCR item")

    @field_validator('position', mode='before')
    def convert_float_to_int(cls, v):
        if v is not None:
            # Ensure all coordinates are rounded to nearest integer, handling NumPy types as well
            return [[round(coord) if isinstance(coord, (float, np.floating)) else int(coord) for coord in point] for point in v]
        return v

class BaseOCREngine(ABC):
    """
    Abstract base class for OCR engines.
    """

    ocr_engine_name: str = "Base OCR Engine"


    @abstractmethod
    def ocr(self, img: ImageLike) -> list[OCRItem]:
        """
        Performs OCR on the given image path synchronously.

        Args:
            img (ImageLike): The image to perform OCR on.

        Returns:
            Any: The OCR result.
        """
        pass


def convert_imagelike_to_type(img: ImageLike, type: Literal["filepath", "numpy", "pil"]) -> Union[str, np.ndarray, Image.Image]:
    """
    Converts the input image-like object to the specified type.

    Args:
        img (ImageLike): The image-like object to convert.
        type (Literal["filepath", "numpy", "pil"]): The type to convert to.

    Returns:
        Union[str, np.ndarray, Image.Image]: The converted image.
    """
    # If the desired type is 'filepath'
    if type == "filepath":
        if isinstance(img, (str, PathLike)):
            # Already a filepath
            return str(img)
        else:
            # Create a temporary file to save the image
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                filepath = tmp_file.name
            if isinstance(img, Image.Image):
                img.save(filepath)
            elif isinstance(img, np.ndarray):
                # Save NumPy array using OpenCV
                cv2.imwrite(filepath, img)
            elif isinstance(img, bytes):
                # Convert bytes to PIL Image and save
                pil_img = Image.open(BytesIO(img))
                pil_img.save(filepath)
            else:
                raise TypeError("Unsupported image type for conversion to filepath.")
            return filepath

    # If the desired type is 'pil'
    elif type == "pil":
        if isinstance(img, Image.Image):
            return img  # Already a PIL image
        elif isinstance(img, np.ndarray):
            # Convert from OpenCV format (BGR) to PIL format (RGB)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(img_rgb)
            return pil_img
        elif isinstance(img, bytes):
            return Image.open(BytesIO(img))
        elif isinstance(img, (str, PathLike)):
            return Image.open(img)
        else:
            raise TypeError("Unsupported image type for conversion to PIL image.")

    # If the desired type is 'numpy' (OpenCV format)
    elif type == "numpy":
        if isinstance(img, np.ndarray):
            return img  # Already a NumPy array in OpenCV format
        elif isinstance(img, Image.Image):
            # Convert PIL image to NumPy array in OpenCV format (BGR)
            img_rgb = np.array(img)
            img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
            return img_bgr
        elif isinstance(img, bytes):
            # Decode bytes to NumPy array using OpenCV
            nparr = np.frombuffer(img, np.uint8)
            img_cv = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            return img_cv
        elif isinstance(img, (str, PathLike)):
            # Read image from file using OpenCV
            img_cv = cv2.imread(str(img))
            return img_cv
        else:
            raise TypeError("Unsupported image type for conversion to NumPy array.")

    else:
        raise ValueError(f"Unknown target type: {type}")
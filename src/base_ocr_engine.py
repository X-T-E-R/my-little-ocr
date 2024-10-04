from abc import ABC, abstractmethod
from typing import Optional
from pydantic import BaseModel, Field, field_validator
import numpy as np
from src.img_utils import ImageLike, convert_imagelike_to_type
import json

class OCRItem(BaseModel):
    """
    Represents an OCR item containing text and its location.
    """

    text: str = Field(..., description="The text content of the OCR item")
    # 4 points, each represented as a list of 2 integers
    box: Optional[list[list[int]]] = Field(
        None,
        description="The position of the OCR item in the image, represented as a list of 4 points",
    )
    confidence: Optional[float] = Field(
        None, description="The confidence score of the OCR item"
    )

    @field_validator("box", mode="before")
    def convert_float_to_int(cls, v):
        if v is not None:
            # Ensure all coordinates are rounded to nearest integer, handling NumPy types as well
            return [
                [
                    (
                        round(coord)
                        if isinstance(coord, (float, np.floating))
                        else int(coord)
                    )
                    for coord in point
                ]
                for point in v
            ]
        return v

    def dict(self) -> dict:
        """
        Converts the OCR item to a dictionary.
        """
        return self.model_dump()


class OCRResult(BaseModel):
    """
    Represents the result of OCR.
    """

    ocr_items: list[OCRItem] = Field(..., description="The list of OCR items")
    default_confidence_threshold: float = Field(
        0.3, description="The default confidence threshold for filtering OCR items"
    )

    def __post_init__(self):
        self.ocr_items = [
            item
            for item in self.ocr_items
            if item.confidence is not None
            and item.confidence >= self.default_confidence_threshold
        ]

    def filter_by_confidence(self, confidence_threshold: float) -> "OCRResult":
        """
        Filters the OCR items by confidence score.
        """
        return OCRResult(
            ocr_items=[
                item
                for item in self.ocr_items
                if item.confidence is not None
                and item.confidence >= confidence_threshold
            ]
        )

    def to_list(self, text_only: bool = False) -> list:
        """
        Converts the OCR result to a list of strings.
        """
        if text_only:
            return [item.text for item in self.ocr_items]
        else:
            return [item.dict() for item in self.ocr_items]

    def to_string(self, separator: str = " ") -> str:
        """
        Converts the OCR result to a string.
        """
        return separator.join(self.to_list(text_only=True))

    def to_json(self, text_only: bool = False, **kwargs) -> str:
        """
        Converts the OCR result to a JSON string.
        """
        kwargs["ensure_ascii"] = False
        return json.dumps(
            self.to_list(text_only=text_only), **kwargs
        )


class BaseOCREngine(ABC):
    """
    Abstract base class for OCR engines.
    """

    ocr_engine_name: str = "Base OCR Engine"

    @abstractmethod
    def ocr(self, img: ImageLike) -> OCRResult:
        """
        Performs OCR on the given image path synchronously.

        Args:
            img (ImageLike): The image to perform OCR on.

        Returns:
            Any: The OCR result.
        """
        pass

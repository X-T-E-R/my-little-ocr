# MyLittleOCR API Library

## Overview

MyLittleOCR is a unified wrapper for several popular OCR libraries, providing a consistent API that allows developers to seamlessly integrate and switch between different OCR engines without altering their application logic.

## Features

- **Unified API**: A consistent interface for multiple OCR engines, simplifying OCR integration.
- **Multiple OCR Backends**: Supports popular OCR libraries including Tesseract, EasyOCR, PaddleOCR, WeChat OCR, Surya, and RapidOCR.
- **Flexible Switching**: Easily switch between OCR backends based on project requirements.
- **Customizable**: Fine-tune accuracy and performance by adjusting parameters for each OCR engine.

## Installation

Install MyLittleOCR using pip:

```bash
pip install ml_ocr
```

## Supported OCR Libraries

Below is a list of supported OCR libraries along with their licenses, project URLs, and usage examples with optional parameters.

| OCR Engine   | License    | Project URL                                                |
| ------------ | ---------- | ---------------------------------------------------------- |
| Tesseract    | Apache 2.0 | [Tesseract](https://github.com/madmaze/pytesseract)        |
| EasyOCR      | Apache 2.0 | [EasyOCR](https://github.com/JaidedAI/EasyOCR)             |
| WeChat OCR   | Unknown    | [WeChat OCR](https://github.com/kanadeblisst00/wechat_ocr) |
| Surya        | GPL 3.0    | [Surya](https://github.com/VikParuchuri/surya)             |
| RapidOCR     | Apache 2.0 | [RapidOCR](https://github.com/RapidAI/RapidOCR)            |

### Tesseract

- **License**: Apache 2.0
- **Project URL**: [Tesseract](https://github.com/madmaze/pytesseract)

To install Tesseract, first ensure you have the Tesseract binary installed. You can download it from [here](https://tesseract-ocr.github.io/tessdoc/#binaries). Then install the Python wrapper:

```bash
pip install pytesseract
```

#### Usage with Optional Parameters

The `TesseractEngine` class can be instantiated with the following optional parameters:

- `tesseract_command`: Path to the Tesseract executable. If not provided, it attempts to find it automatically.
- `default_langs`: A list of language codes or names. Default is `["eng", "chi_sim"]`.


> **Note**: You can use language names like 'English', 'eng', or 'en'. The program automatically converts them using the `iso639` library.

### EasyOCR

- **License**: Apache 2.0
- **Project URL**: [EasyOCR](https://github.com/JaidedAI/EasyOCR)

Install EasyOCR using:

```bash
pip install easyocr
```

#### Usage with Optional Parameters

The `EasyOCREngine` class accepts the following optional parameters:

- `default_langs`: A list of language codes or names. Default is `["ch_sim", "en"]`.
- Additional parameters supported by EasyOCR's `Reader` class (see [EasyOCR Documentation](https://www.jaided.ai/easyocr/documentation/)).


### WeChat OCR

- **License**: Unknown (utilizes components from WeChat, a closed-source project. Use with caution and do not use for commercial purposes. Only supported on Windows.)
- **Project URL**: [WeChat OCR](https://github.com/kanadeblisst00/wechat_ocr)

Install WeChat OCR using:

```bash
pip install wechat_ocr
```

#### Usage

The `WechatOCREngine` does not require additional optional parameters for instantiation.


### Surya

- **License**: GPL 3.0
- **Project URL**: [Surya](https://github.com/VikParuchuri/surya)

Install Surya using:

```bash
pip install surya-ocr
```

#### Usage with Optional Parameters

The `SuryaEngine` class can be instantiated with the following optional parameters:

- `default_langs`: A list of language codes or names. Default is `["en", "zh", "_math"]`.
- Additional parameters can be passed via `**kwargs`.


### RapidOCR

- **License**: Apache 2.0
- **Project URL**: [RapidOCR](https://github.com/RapidAI/RapidOCR)

Install RapidOCR using:

```bash
pip install rapidocr_onnxruntime
```

#### Usage with Optional Parameters

The `RapidOCREngine` class accepts the following optional parameters:

- `det_model`: Detection model path or name. Default is `"ch_PP-OCRv4_det_infer.onnx"`.
- `rec_model`: Recognition model path or name. Default is `"ch_PP-OCRv4_rec_infer.onnx"`.
- Additional parameters supported by `RapidOCR` (see [RapidOCR API Documentation](https://rapidai.github.io/RapidOCRDocs/install_usage/api/RapidOCR/)).

> **Note**: The models will be automatically downloaded if not present. You can specify custom model paths as needed.

## Quick Start

Here's an example of how to use the MyLittleOCR API to extract text from an image:

```python
from ocr_engines import get_engine_class

# Get an instance of the desired OCR engine (e.g., 'tesseract', 'easyocr', 'paddleocr', 'wechat_ocr', 'surya', 'rapidocr')
ocr_engine = get_engine_class('tesseract')

# Extract text from an image
ocr_result = ocr_engine.ocr('/path/to/image.jpg')

# Convert OCR result to a list and print it
print("OCR Result:", ocr_result.to_list())
```

## Ways to Interact with the API

There are two main ways to interact with the API in MyLittleOCR:

### 1. Engine Management-Based API Interaction

- **Get All Engines**: Use `get_all_engines()` to retrieve all registered OCR engines.

  ```python
  from ocr_engines import get_all_engines

  engines = get_all_engines()
  for engine_name, engine_class in engines.items():
      print(f"Engine Name: {engine_name}")
      engine_instance = engine_class()
      result = engine_instance.ocr('/path/to/image.jpg')
      print(result.to_list())
  ```

- **Get Engine Instance**: Use `get_engine_instance(engine_name, **kwargs)` to get an instance of a specific OCR engine with optional parameters.

  ```python
  from ocr_engines import get_engine_instance

  engine_instance = get_engine_instance('easyocr')
  ```

- **Get Engine Class**: Use `get_engine_class(engine_name)` to get the class of a specific OCR engine.

  ```python
  from ocr_engines import get_engine_class

  EasyOCREngine = get_engine_class('easyocr')
  ```

### 2. Direct Import from Specific Library

Directly import the engine class from the specific OCR engine module, then instantiate and use it.

```python
from ocr_engines.easyocr_engine import EasyOCREngine

engine_instance = EasyOCREngine(
    default_langs=['English', 'Korean'],
    gpu=False
)
```

## Working with OCR Results

The `OCRResult` class represents OCR results and provides methods to process and filter them.

### Initialization

Create an `OCRResult` instance by providing a list of `OCRItem` instances.

```python
from my_little_ocr.base_engine.base_ocr_engine import OCRResult, OCRItem

ocr_items = [
    OCRItem(
        text="example",
        box=[[0, 0], [1, 0], [1, 1], [0, 1]],
        confidence=0.9
    )
]
ocr_result = OCRResult(ocr_items=ocr_items)
```

### Filtering Results

Use `filter_by_confidence(confidence_threshold)` to filter OCR results based on confidence scores.

```python
filtered_result = ocr_result.filter_by_confidence(0.8)
```

### Converting Results to List

Use `to_list(text_only=False)` to convert OCR results to a list. Set `text_only=True` to retrieve only the text content.

```python
text_list = ocr_result.to_list(text_only=True)
full_list = ocr_result.to_list(text_only=False)
```

These methods provide flexible ways to manage and utilize OCR results.

## Base OCREngine Class

Below is the abstract base class for all OCR engines:

```python
from abc import ABC, abstractmethod
from typing import Union
from PIL import Image
import numpy as np

ImageLike = Union[str, bytes, np.ndarray, Image.Image]

class BaseOCREngine(ABC):
    """
    Abstract base class for OCR engines.
    """

    ocr_engine_name: str = "Base OCR Engine"

    @abstractmethod
    def ocr(self, img: ImageLike) -> OCRResult:
        """
        Performs OCR on the given image.

        Args:
            img (ImageLike): The image to perform OCR on.

        Returns:
            OCRResult: The OCR result.
        """
        pass
```

The input `img` supports multiple formats:

- File path as a string
- Bytes
- NumPy array (`np.ndarray`)
- PIL Image (`Image.Image`)

## Contributing

Contributions are welcome! If you'd like to add support for more OCR libraries or suggest improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

**Note**: Individual OCR engines may have different licenses. Please refer to their respective project pages for more details.

## Acknowledgments

We would like to thank the following libraries that make this project possible:

- **Pydantic**
- **GitPython**
- **iso639-lang**

And all the OCR libraries mentioned above.

## Credits


Thanks to all the contributors and maintainers of the OCR libraries that were used in this project.

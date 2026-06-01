"""
Image preprocessing utilities for VitalLens.
"""

from typing import Tuple
import numpy as np
from PIL import Image


def preprocess_image(image: Image.Image, target_size: Tuple[int, int] = (224, 224)) -> np.ndarray:
    """
    Preprocess a PIL image for model inference.

    Steps:
    - Convert to RGB
    - Resize to target size
    - Normalize to [0, 1]
    - Add batch dimension
    """
    if image is None:
        raise ValueError("image is required")

    img = image.convert("RGB").resize(target_size)
    arr = np.asarray(img, dtype=np.float32) / 255.0
    # Add batch dimension: (1, H, W, C)
    return np.expand_dims(arr, axis=0)

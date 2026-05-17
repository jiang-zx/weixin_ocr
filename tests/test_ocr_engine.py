import numpy as np
import pytest
import os
import sys

# Add the project root to sys.path to ensure ocr_engine can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_ocr_provider():
    # Create a black image
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    
    # This should fail initially because LocalOCRProvider is not defined
    from ocr_engine import LocalOCRProvider
    provider = LocalOCRProvider()
    
    # Running on black image should return an empty list or at least be a list
    results = provider.ocr(img)
    assert isinstance(results, list)

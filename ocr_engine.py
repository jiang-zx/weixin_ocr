from paddleocr import PaddleOCR
import numpy as np

class LocalOCRProvider:
    def __init__(self):
        # Initialize PaddleOCR model (downloaded automatically on first run)
        # lang="ch" supports Chinese and English
        # Disable MKLDNN to avoid compatibility issues in some environments
        self.ocr_model = PaddleOCR(use_textline_orientation=True, lang="ch", enable_mkldnn=False)

    def ocr(self, image: np.ndarray) -> list:
        """
        Returns a list of dictionaries: [{'text': str, 'box': [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]}, ...]
        """
        result = self.ocr_model.predict(image)
        parsed_results = []
        if not result or not result[0]:
            return parsed_results
            
        for line in result[0]:
            box = line[0]
            text = line[1][0]
            parsed_results.append({
                'text': text,
                'box': box
            })
        return parsed_results

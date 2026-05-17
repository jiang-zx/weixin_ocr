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
        if not result:
            return parsed_results
        
        # Parse results from PaddleOCR 3.x/Paddlex output
        try:
            for res in result:
                if 'dt_polys' in res and 'rec_texts' in res:
                    for box, text in zip(res['dt_polys'], res['rec_texts']):
                        # box is a numpy array of 4 points
                        parsed_results.append({
                            'text': text,
                            'box': box.tolist() if hasattr(box, 'tolist') else box
                        })
                elif 'doc_res' in res:
                    # Alternative path for some pipeline outputs
                    for page in res['doc_res'].get('pages', []):
                        for line in page.get('lines', []):
                            parsed_results.append({
                                'text': line['content'],
                                'box': line['coord']
                            })
        except Exception as e:
            # If parsing fails, we could log it, but for now we return what we have
            pass

        return parsed_results

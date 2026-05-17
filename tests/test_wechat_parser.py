import numpy as np
import pytest
import os
import sys

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from wechat_parser import parse_dialogue

def test_parse_dialogue():
    # Create an image simulating green and white backgrounds
    # BGR format: White is [240, 240, 240], Green is [100, 200, 100]
    img = np.full((500, 541, 3), 240, dtype=np.uint8) # White background (friend)
    img[100:200, :] = [100, 200, 100] # Green background (self)
    
    # Mock OCR results
    # box format: [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    ocr_results = [
        {'text': '12:30', 'box': [[200.0, 10.0], [250.0, 10.0], [250.0, 30.0], [200.0, 30.0]]}, # Time, should be ignored
        {'text': 'Hello', 'box': [[50.0, 50.0], [100.0, 50.0], [100.0, 80.0], [50.0, 80.0]]}, # Friend (white bg)
        {'text': 'Hi there', 'box': [[400.0, 120.0], [480.0, 120.0], [480.0, 150.0], [400.0, 150.0]]} # Self (green bg)
    ]
    
    dialogue = parse_dialogue(ocr_results, img)
    assert len(dialogue) == 2
    assert dialogue[0] == "好友:Hello"
    assert dialogue[1] == "自己:Hi there"

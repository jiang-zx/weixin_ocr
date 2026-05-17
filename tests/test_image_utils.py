import numpy as np
import cv2
import pytest
import os
import sys

# 将当前目录添加到路径以便导入 image_utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from image_utils import image_resize, image_split

def test_image_resize():
    img = np.zeros((1000, 1000, 3), dtype=np.uint8)
    resized = image_resize(img)
    assert resized.shape[1] == 541

def test_image_split_small():
    img = np.zeros((1000, 500, 3), dtype=np.uint8)
    img_bytes = cv2.imencode('.jpg', img)[1].tobytes()
    splits = image_split(img_bytes)
    assert len(splits) == 1

def test_image_split_large():
    img = np.zeros((3000, 500, 3), dtype=np.uint8)
    img_bytes = cv2.imencode('.jpg', img)[1].tobytes()
    splits = image_split(img_bytes)
    assert len(splits) == 2

import cv2
import math
import numpy as np

def image_resize(image):
    (h, w) = image.shape[:2]
    WIDTH = 541
    r = WIDTH / float(w)
    dim = (WIDTH, int(h * r))
    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

def image_split(imageBytes):
    image = cv2.imdecode(np.frombuffer(imageBytes, np.uint8), cv2.IMREAD_COLOR)
    (h, w) = image.shape[:2]
    sub_images = []
    if h >= 2000:
        num = int(math.ceil(h / 2000))
        height = int(h / num)
        for i in range(num):
            startY = i * height
            endY = (i + 1) * height
            dim = (w, endY - startY)
            if dim[0] <= w and dim[1] <= h:
                sub_image = cv2.resize(image[startY:endY, 0:w], dim, interpolation=cv2.INTER_AREA)
                sub_images.append(sub_image)
    else:
        sub_images.append(image)
    return sub_images

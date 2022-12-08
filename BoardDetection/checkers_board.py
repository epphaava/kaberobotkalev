from math import floor

from BoardDetection.constants import BOARD_SIZE
from BoardDetection.constants import SQUARE_SIZE
import numpy as np
import cv2


class Square:
    def __init__(self, position, raw_img):
        self.position = position
        self.img = raw_img


class CheckersBoard():
    def __init__(self, img):
        self.img = img

    def square_at(self, i):
        y = floor((i / 8)) * SQUARE_SIZE
        x = (i % 8) * SQUARE_SIZE
        return Square(i, self.img[y:y + SQUARE_SIZE, x:x + SQUARE_SIZE])

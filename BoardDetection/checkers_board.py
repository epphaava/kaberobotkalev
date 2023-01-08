from math import floor

from BoardDetection.variables.constants import SQUARE_SIZE


class Square:
    def __init__(self, position, raw_img):
        self.position = position
        self.img = raw_img
    def get_img(self):
        return self.img


class CheckersBoard():
    def __init__(self, img):
        self.img = img

    def square_at(self, i):
        y = floor((i / 8)) * SQUARE_SIZE
        x = (i % 8) * SQUARE_SIZE
        return Square(i, self.img[y:y + SQUARE_SIZE, x:x + SQUARE_SIZE])

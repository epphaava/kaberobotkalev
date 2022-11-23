import cv2
import numpy as np

from BoardDetection.checkers_board import CheckersBoard
from BoardDetection.constants import BOARD_SIZE, GREEN_LOW_VALUES, GREEN_HIGH_VALUES, RED_LOW_VALUES, RED_HIGH_VALUES
from BoardDetection.perspective_transform import get_checkersboard_perspective_transform


def detectcolor(sq, detector):
    sq_hsv = cv2.cvtColor(sq.img, cv2.COLOR_BGR2HSV)

    thresholdedgreen = cv2.inRange(sq_hsv, GREEN_LOW_VALUES, GREEN_HIGH_VALUES)
    thresholdedred = cv2.inRange(sq_hsv, RED_LOW_VALUES, RED_HIGH_VALUES)
    thresholdedgreen = cv2.bitwise_not(thresholdedgreen)
    thresholdedred = cv2.bitwise_not(thresholdedred)
    height, width = thresholdedred.shape
    thresholdedred = cv2.rectangle(thresholdedred, (0, 0), (width - 1, height - 1), (255, 255, 255), 2)
    thresholdedgreen = cv2.rectangle(thresholdedgreen, (0, 0), (width - 1, height - 1), (255, 255, 255), 2)

    redpoints = detector.detect(thresholdedred)
    greenpoints = detector.detect(thresholdedgreen)

    if redpoints:
        return "r"
    if greenpoints:
        return "g"
    return "-"


class Camera:
    def __init__(self, camera):
        self._capture = camera

    def current_chessboard_frame(self):
        _, frame = self._capture.read()
        frame = cv2.blur(frame, (3, 3))
        m = get_checkersboard_perspective_transform()
        img = cv2.warpPerspective(frame, m, (BOARD_SIZE, BOARD_SIZE))
        return CheckersBoard(img)

    def current_raw_frame(self):
        _, frame = self._capture.read()
        return frame

    def current_board(self):
        blobparams = cv2.SimpleBlobDetector_Params()
        blobparams.filterByArea = True
        blobparams.minArea = 10
        blobparams.maxArea = 1E5
        blobparams.filterByCircularity = False
        blobparams.filterByInertia = False
        blobparams.filterByConvexity = False
        blobparams.minDistBetweenBlobs = 5
        detector = cv2.SimpleBlobDetector_create(blobparams)

        ccf = self.current_chessboard_frame()
        cb = ["-"] * 64
        for i in range(64):
            sq = ccf.square_at(i)
            cb[i] = detectcolor(sq, detector)
        return cb

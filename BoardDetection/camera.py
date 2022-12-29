import cv2

from BoardDetection.checkers_board import CheckersBoard
from BoardDetection.constants import BOARD_SIZE, ROBOT_LOW_VALUES, ROBOT_HIGH_VALUES, OPPONENT_LOW_VALUES, \
    OPPONENT_HIGH_VALUES, OPPONENT_CROWN_LOW_VALUES, OPPONENT_CROWN_HIGH_VALUES, ROBOT_CROWN_HIGH_VALUES, \
    ROBOT_CROWN_LOW_VALUES
from BoardDetection.perspective_transform import get_checkersboard_perspective_transform


def detectcolor(sq):
    img = sq.img
    img = img[20:40, 20:40]

    thresholded_opponent = cv2.inRange(img, OPPONENT_LOW_VALUES, OPPONENT_HIGH_VALUES)
    thresholded_robot = cv2.inRange(img, ROBOT_LOW_VALUES, ROBOT_HIGH_VALUES)

    thresholded_opponent_crown = cv2.inRange(img, OPPONENT_CROWN_LOW_VALUES, OPPONENT_CROWN_HIGH_VALUES)
    thresholded_robot_crown = cv2.inRange(img, ROBOT_CROWN_LOW_VALUES, ROBOT_CROWN_HIGH_VALUES)

    if cv2.countNonZero(thresholded_opponent) > 0:
        return "o"
    if cv2.countNonZero(thresholded_robot) > 0:
        return "x"
    if cv2.countNonZero(thresholded_opponent_crown) > 0:
        return "p"
    if cv2.countNonZero(thresholded_robot_crown) > 0:
        return "y"
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
        ccf = self.current_chessboard_frame()
        cb = ["-"] * 64
        for i in range(64):
            sq = ccf.square_at(i)
            cb[i] = detectcolor(sq)
        f = open("./BoardDetection/board_array.txt", "w")
        f.writelines([f"{line}" for line in cb])
        f.close()
        return cb

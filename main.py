import time

import cv2
from BoardDetection.camera import Camera
import gameplay.next_turn as next_turn

camera = cv2.VideoCapture
BOARD_SIZE = 480
SQUARE_SIZE = 60


def init():
    global camera
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)


def main():
    checkerscam = Camera(camera)

    while True:
        # camera is on the side of the robot, opposite the human player
        ret, frame = camera.read()
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)

        # press ESC to quit program
        if k % 256 == 27:
            print("Escape hit, closing...")
            break

        # press SPACE to get next move of robot
        elif k % 256 == 32:
            try:
                board = checkerscam.current_board()
                print(board)
                next_turn.text_board()
            except Exception as e:
                #print("something went wrong ", e)
                raise e

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    init()
    main()

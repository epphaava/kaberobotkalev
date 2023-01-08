import time

import cv2
from BoardDetection.camera import Camera
import gameplay.next_turn as next_turn
import serial
from BoardDetection.variables.constants import camera_index
from BoardDetection.variables.constants import arduino_com

camera = cv2.VideoCapture

def init():
    global camera
    camera = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)


def main():
    checkerscam = Camera(camera)

    baud_rate = 9600
    ser = serial.Serial(arduino_com, baud_rate)
    time.sleep(2)
    ret, frame = camera.read()
    next_turn.calibrate(ser, checkerscam)
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
                next_turn.text_board(ser)
                next_turn.calibrate(ser, checkerscam)
            except Exception as e:
                print("something went wrong ", e)

    camera.release()
    ser.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    init()
    main()

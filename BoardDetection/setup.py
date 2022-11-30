import time

import cv2

from BoardDetection.camera import Camera
from perspective_transform import calibrate_camera

camera = cv2.VideoCapture

lH = 0
lS = 0
lV = 0
hH = 255
hS = 255
hV = 255


def updatelH(new):
    global lH
    lH = new


def updatelS(new):
    global lS
    lS = new


def updatelV(new):
    global lV
    lV = new


def updatehH(new):
    global hH
    hH = new


def updatehS(new):
    global hS
    hS = new


def updatehV(new):
    global hV
    hV = new


def init():
    global camera
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)


def main():
    try:
        print("Seadista kaamera keskele")
        checkers_camera = Camera(camera)
        while True:
            frame = checkers_camera.current_raw_frame()
            height, width = frame.shape[:2]
            cv2.line(frame, (int(width / 2), 0), (int(width / 2), height), (255, 0, 0), 2)
            cv2.line(frame, (0, int(height / 2)), (width, int(height / 2)), (255, 0, 0), 2)
            cv2.imshow("center", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        print("Seadistame transform")
        calibrate_camera(camera)
        while True:
            transformed = checkers_camera.current_chessboard_frame().img
            cv2.imshow("transformed", transformed)
            if cv2.waitKey() & 0xFF == ord('y'):
                break
            calibrate_camera(camera)

    except KeyboardInterrupt:
        print("closing program")
    finally:
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    init()
    main()

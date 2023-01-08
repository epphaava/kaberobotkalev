import cv2
import numpy as np

from BoardDetection.camera import Camera
from BoardDetection.perspective_transform import calibrate_camera
from BoardDetection.variables.constants import camera_index

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
    camera = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)


def main():
    try:
        print("Align the board with the cross")
        checkers_camera = Camera(camera)
        while True:
            frame = checkers_camera.current_raw_frame()
            height, width = frame.shape[:2]
            cv2.line(frame, (int(width / 2), 0), (int(width / 2), height), (255, 0, 0), 2)
            cv2.line(frame, (0, int(height / 2)), (width, int(height / 2)), (255, 0, 0), 2)
            cv2.imshow("center", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        print("Confirm transformation")
        calibrate_camera(camera)
        while True:
            transformed = checkers_camera.current_chessboard_frame().img
            cv2.imshow("transformed", transformed)
            if cv2.waitKey() & 0xFF == ord('y'):
                break
            calibrate_camera(camera)
        cv2.destroyAllWindows()
        cv2.namedWindow("Thresholded")
        cv2.createTrackbar("lH", "Thresholded", np.load("BoardDetection/variables/robotlowerlimits.npy")[0], 255, updatelH)
        cv2.createTrackbar("lS", "Thresholded", np.load("BoardDetection/variables/robotlowerlimits.npy")[1], 255, updatelS)
        cv2.createTrackbar("lV", "Thresholded", np.load("BoardDetection/variables/robotlowerlimits.npy")[2], 255, updatelV)
        cv2.createTrackbar("hH", "Thresholded", np.load("BoardDetection/variables/robotupperlimits.npy")[0], 255, updatehH)
        cv2.createTrackbar("hS", "Thresholded", np.load("BoardDetection/variables/robotupperlimits.npy")[1], 255, updatehS)
        cv2.createTrackbar("hV", "Thresholded", np.load("BoardDetection/variables/robotupperlimits.npy")[2], 255, updatehV)
        print("Threshold the Robot's Pieces")
        while True:
            frame = checkers_camera.current_chessboard_frame().img
            cv2.imshow("unthresholded", frame)
            lowerLimits = np.array([lH, lS, lV])
            upperLimits = np.array([hH, hS, hV])
            thresholded = cv2.inRange(frame, lowerLimits, upperLimits)
            cv2.imshow("Thresholded confirmation", thresholded)
            if cv2.waitKey(1) & 0xFF == ord('y'):
                np.save("BoardDetection/variables/robotlowerlimits.npy", lowerLimits)
                np.save("BoardDetection/variables/robotupperlimits.npy", upperLimits)
                break
        cv2.destroyAllWindows()
        cv2.namedWindow("Thresholded")
        cv2.createTrackbar("lH", "Thresholded", np.load("BoardDetection/variables/opponentlowerlimits.npy")[0], 255, updatelH)
        cv2.createTrackbar("lS", "Thresholded", np.load("BoardDetection/variables/opponentlowerlimits.npy")[1], 255, updatelS)
        cv2.createTrackbar("lV", "Thresholded", np.load("BoardDetection/variables/opponentlowerlimits.npy")[2], 255, updatelV)
        cv2.createTrackbar("hH", "Thresholded", np.load("BoardDetection/variables/opponentupperlimits.npy")[0], 255, updatehH)
        cv2.createTrackbar("hS", "Thresholded", np.load("BoardDetection/variables/opponentupperlimits.npy")[1], 255, updatehS)
        cv2.createTrackbar("hV", "Thresholded", np.load("BoardDetection/variables/opponentupperlimits.npy")[2], 255, updatehV)
        print("Threshold the Opponent's Pieces")
        while True:
            frame = checkers_camera.current_chessboard_frame().img
            cv2.imshow("unthresholded", frame)
            lowerLimits = np.array([lH, lS, lV])
            upperLimits = np.array([hH, hS, hV])
            thresholded = cv2.inRange(frame, lowerLimits, upperLimits)
            cv2.imshow("Thresholded confirmation", thresholded)
            if cv2.waitKey(1) & 0xFF == ord('y'):
                np.save("BoardDetection/variables/opponentlowerlimits.npy", lowerLimits)
                np.save("BoardDetection/variables/opponentupperlimits.npy", upperLimits)
                break
        cv2.destroyAllWindows()
        cv2.namedWindow("Thresholded")
        cv2.createTrackbar("lH", "Thresholded", np.load("BoardDetection/variables/robotcrownlowerlimits.npy")[0], 255, updatelH)
        cv2.createTrackbar("lS", "Thresholded", np.load("BoardDetection/variables/robotcrownlowerlimits.npy")[1], 255, updatelS)
        cv2.createTrackbar("lV", "Thresholded", np.load("BoardDetection/variables/robotcrownlowerlimits.npy")[2], 255, updatelV)
        cv2.createTrackbar("hH", "Thresholded", np.load("BoardDetection/variables/robotcrownupperlimits.npy")[0], 255, updatehH)
        cv2.createTrackbar("hS", "Thresholded", np.load("BoardDetection/variables/robotcrownupperlimits.npy")[1], 255, updatehS)
        cv2.createTrackbar("hV", "Thresholded", np.load("BoardDetection/variables/robotcrownupperlimits.npy")[2], 255, updatehV)
        print("Threshold the Robot's Crowns")
        while True:
            frame = checkers_camera.current_chessboard_frame().img
            cv2.imshow("unthresholded", frame)
            lowerLimits = np.array([lH, lS, lV])
            upperLimits = np.array([hH, hS, hV])
            thresholded = cv2.inRange(frame, lowerLimits, upperLimits)
            cv2.imshow("Thresholded confirmation", thresholded)
            if cv2.waitKey(1) & 0xFF == ord('y'):
                np.save("BoardDetection/variables/robotcrownlowerlimits.npy", lowerLimits)
                np.save("BoardDetection/variables/robotcrownupperlimits.npy", upperLimits)
                break
        cv2.destroyAllWindows()
        cv2.namedWindow("Thresholded")
        cv2.createTrackbar("lH", "Thresholded", np.load("BoardDetection/variables/opponentcrownlowerlimits.npy")[0], 255, updatelH)
        cv2.createTrackbar("lS", "Thresholded", np.load("BoardDetection/variables/opponentcrownlowerlimits.npy")[1], 255, updatelS)
        cv2.createTrackbar("lV", "Thresholded", np.load("BoardDetection/variables/opponentcrownlowerlimits.npy")[2], 255, updatelV)
        cv2.createTrackbar("hH", "Thresholded", np.load("BoardDetection/variables/opponentcrownupperlimits.npy")[0], 255, updatehH)
        cv2.createTrackbar("hS", "Thresholded", np.load("BoardDetection/variables/opponentcrownupperlimits.npy")[1], 255, updatehS)
        cv2.createTrackbar("hV", "Thresholded", np.load("BoardDetection/variables/opponentcrownupperlimits.npy")[2], 255, updatehV)
        print("Threshold the Opponent's Crowns")
        while True:
            frame = checkers_camera.current_chessboard_frame().img
            cv2.imshow("unthresholded", frame)
            lowerLimits = np.array([lH, lS, lV])
            upperLimits = np.array([hH, hS, hV])
            thresholded = cv2.inRange(frame, lowerLimits, upperLimits)
            cv2.imshow("Thresholded confirmation", thresholded)
            if cv2.waitKey(1) & 0xFF == ord('y'):
                np.save("BoardDetection/variables/opponentcrownlowerlimits.npy", lowerLimits)
                np.save("BoardDetection/variables/opponentcrownupperlimits.npy", upperLimits)
                break

    except KeyboardInterrupt:
        print("closing program")
    finally:
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    init()
    main()

import cv2
import numpy as np

from BoardDetection.camera import Camera
from BoardDetection.checkers_board import CheckersBoard

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
    camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)


kernelsize = 3


def updateKernelsize(new):
    global kernelsize
    if new % 2 == 0:
        kernelsize = new + 1

    else:
        kernelsize = new
    cv2.setTrackbarPos("Kernel Size", "BGR", kernelsize)


def main():
    try:
        cv2.namedWindow("Thresholded")
        cv2.namedWindow("BGR")
        cv2.namedWindow("HSV")
        cv2.createTrackbar("lH", "Thresholded", lH, 255, updatelH)
        cv2.createTrackbar("lS", "Thresholded", lS, 255, updatelS)
        cv2.createTrackbar("lV", "Thresholded", lV, 255, updatelV)
        cv2.createTrackbar("hH", "Thresholded", hH, 255, updatehH)
        cv2.createTrackbar("hS", "Thresholded", hS, 255, updatehS)
        cv2.createTrackbar("hV", "Thresholded", hV, 255, updatehV)
        cv2.createTrackbar("Kernel Size", "BGR", int(kernelsize), 100, updateKernelsize)

        blobparams = cv2.SimpleBlobDetector_Params()
        blobparams.filterByArea = True
        blobparams.minArea = 200
        blobparams.maxArea = 1E5
        blobparams.filterByCircularity = False
        blobparams.filterByInertia = False
        blobparams.filterByConvexity = False
        blobparams.minDistBetweenBlobs = 5
        detector = cv2.SimpleBlobDetector_create(blobparams)
        checkerscam = Camera(camera)
        while True:
            frame = checkerscam.current_chessboard_frame().img
            kernel = (kernelsize, kernelsize)
            frame = cv2.blur(frame, kernel)
            hsv = frame
            cv2.imshow("HSV", hsv)
            lowerLimits = np.array([lH, lS, lV])
            upperLimits = np.array([hH, hS, hV])
            thresholded = cv2.inRange(frame, lowerLimits, upperLimits)
            cv2.imshow("Thresholded", thresholded)
            thresholdedflip = cv2.bitwise_not(thresholded)

            keypoints = detector.detect(thresholdedflip)
            for keypoint in keypoints:
                cv2.putText(frame, str(round(keypoint.pt[0], 1)) + "," + str(round(keypoint.pt[1], 1)), (int(
                    keypoint.pt[0]), int(keypoint.pt[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            frame = cv2.drawKeypoints(
                frame, keypoints, None, (0, 255, 0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            height, width = frame.shape[:2]
            cv2.line(frame, (int(width / 2), 0), (int(width / 2), height), (255, 0, 0), 2)
            cv2.line(frame, (0, int(height / 2)), (width, int(height / 2)), (255, 0, 0), 2)
            cv2.imshow("BGR", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        print("closing program")
    finally:
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    init()
    main()

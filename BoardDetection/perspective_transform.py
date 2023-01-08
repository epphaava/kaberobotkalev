import cv2
import numpy as np

perspective_transform_path = "BoardDetection/checkersboard_perspective_transform.npy"


def get_checkersboard_perspective_transform():
    try:
        m = np.load(perspective_transform_path)
        return m
    except IOError:
        print("need to calibrate camera")

def calibrate_camera(camera):
    board_size = (7, 7)
    _, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    found, corners = cv2.findChessboardCorners(gray, board_size,
                                               flags=cv2.CALIB_CB_NORMALIZE_IMAGE | cv2.CALIB_CB_ADAPTIVE_THRESH)
    if found:
        z = corners.reshape((49, 2))
        p = []
        q = []
        p.append(z[0])
        q.append((60.0, 60.0))

        p.append(z[6])
        q.append((420, 60))

        p.append(z[42])
        q.append((60, 420))

        p.append(z[48])
        q.append((420, 420.0))

        q = np.array(q, np.float32)
        p = np.array(p, np.float32).reshape(q.shape)
        m = cv2.getPerspectiveTransform(p, q)
        np.save(perspective_transform_path, m)



def main():
    calibrate_camera()


if __name__ == '__main__':
    main()

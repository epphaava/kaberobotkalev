import numpy as np
import cv2
from itertools import product

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

perspective_transform_path = "checkersboard_perspective_transform.npy"


def get_checkersboard_perspective_transform():
    try:
        m = np.load(perspective_transform_path)
        return m
    except IOError:
        print("need to calibrate camera")


def calibrate_camera():
    board_size = (7, 7)
    camera = cv2.VideoCapture(1,cv2.CAP_DSHOW)

    _, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    found, corners = cv2.findChessboardCorners(gray, board_size,
                                               flags=cv2.CALIB_CB_NORMALIZE_IMAGE | cv2.CALIB_CB_ADAPTIVE_THRESH)
    if found:
        z = corners.reshape((49, 2))
        x_train = np.array(list(product(np.linspace(-3, 3, 7), np.linspace(-3, 3, 7))))

        poly = PolynomialFeatures(degree=4)
        x_train = poly.fit_transform(x_train)

        m_x = LinearRegression()
        m_x.fit(x_train, z[:, 0])

        m_y = LinearRegression()
        m_y.fit(x_train, z[:, 1])

        def predict(i, j):
            features = poly.fit_transform(np.array([i, j]).reshape(1, -1))
            return m_x.predict(features), m_y.predict(features)

        p = []
        q = []

        p.append(predict(-4.0, -4.0))
        q.append((0.0, 0.0))

        p.append(predict(-4.0, 4.0))
        q.append((0.0, 480.0))

        p.append(predict(4.0, -4.0))
        q.append((480.0, 0.0))

        p.append(predict(4.0, 4.0))
        q.append((480.0, 480.0))

        q = np.array(q, np.float32)
        p = np.array(p, np.float32).reshape(q.shape)
        ind = np.lexsort((p[:, 1], p[:, 0]))
        p = p[ind]


        m = cv2.getPerspectiveTransform(p, q)
        np.save(perspective_transform_path, m)


def main():
    calibrate_camera()


if __name__ == '__main__':
    main()

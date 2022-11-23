import cv2
import numpy as np
from itertools import product
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from scipy.spatial.distance import euclidean

camera = cv2.VideoCapture


def init():
    global camera
    camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)


def get_chessboard_perspective_transform():
    board_size = (7, 7)

    _, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    found, corners = cv2.findChessboardCorners(gray, board_size,
                                               flags=cv2.CALIB_CB_NORMALIZE_IMAGE | cv2.CALIB_CB_ADAPTIVE_THRESH)
    if found:
        z = corners.reshape((49, 2))
        X_train = np.array(list(product(np.linspace(-3, 3, 7), np.linspace(-3, 3, 7))))

        poly = PolynomialFeatures(degree=4)
        X_train = poly.fit_transform(X_train)

        m_x = LinearRegression()
        m_x.fit(X_train, z[:, 0])

        m_y = LinearRegression()
        m_y.fit(X_train, z[:, 1])

        def predict(i, j):
            features = poly.fit_transform(np.array([i, j]).reshape(1, -1))
            return m_x.predict(features), m_y.predict(features)

        P = []
        Q = []

        P.append(predict(-4.0, -4.0))
        Q.append((0.0, 0.0))

        P.append(predict(-4.0, 4.0))
        Q.append((0.0, 480.0))

        P.append(predict(4.0, -4.0))
        Q.append((480.0, 0.0))

        P.append(predict(4.0, 4.0))
        Q.append((480.0, 480.0))

        Q = np.array(Q, np.float32)
        P = np.array(P, np.float32).reshape(Q.shape)
        ind = np.lexsort((P[:, 1], P[:, 0]))
        P = P[ind]

        M = cv2.getPerspectiveTransform(P, Q)
        return M


def main():
    try:
        M = get_chessboard_perspective_transform()
        while True:
            ret, frame = camera.read()
            cv2.imshow('frame', frame)
            img = cv2.warpPerspective(frame, M, (480, 480))
            cv2.imshow('warped', img)
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

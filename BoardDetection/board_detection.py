import cv2

from BoardDetection.camera import Camera

camera = cv2.VideoCapture

def init():
    global camera
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

def main():
    try:
        checkerscam = Camera(camera)
        while True:
            _, frame = camera.read()
            cv2.imshow("original", checkerscam.current_raw_frame())
            checkersframe = checkerscam.current_chessboard_frame()
            cv2.imshow("checkersframe", checkersframe.img)
            laud = checkerscam.current_board()

            print(laud)
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
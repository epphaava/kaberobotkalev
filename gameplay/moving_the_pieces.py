import time

import cv2
import numpy as np

# use this method to move the piece through corners to the given destination in best_moves

# this method assumes the removed pieces will be on the right side of the board

# from the perspective of the robot
# 7 - forward and left
# 0 - forward
# 1 - forward and right
# 2 - right
# 5 - back and right
# 4 - back
# 3 - back and left
# 6 - left

# 9 - magnet ON
# 8 - magnet OFF

# MOVEMENT FINISHED

magnet_current_position = 73


def move(move, piece):
    global magnet_current_position

    moves = []

    current_position = int(move['current_position'])
    goal_position = move['goal_position']

    magnet_to_current_position(current_position, moves)


    if goal_position == "*remove":



        # switch regular piece for a crown or remove a piece
        # in both cases the piece needs to be moved off the board
        # currently the crown has to be added by hand as we don't know where we could keep the crown pieces
        moves.append('2')
        #for i in range(math.ceil((current_position // 10) / 2)):
        #    moves.append('1')
        #    moves.append('7')

    # if only one move to make
    elif piece == "regular":

        current_row = int(current_position) // 10
        current_column = int(current_position) % 10

        goal_row = int(goal_position) // 10
        goal_column = int(goal_position) % 10

        # if the piece is moving forward

        if current_column < goal_column:
            if current_row > goal_row:
                for i in range(abs(goal_column - current_column)):
                    moves.append('1')
            else:
                for i in range(abs(goal_column - current_column)):
                    moves.append('5')
        else:
            if current_row > goal_row:
                for i in range(abs(goal_column - current_column)):
                    moves.append('7')
            else:
                for i in range(abs(goal_column - current_column)):
                    moves.append('3')

        # if moving back (possible if it is a crown)
    elif piece == "*crown":

        current_row = int(current_position) // 10
        current_column = int(current_position) % 10

        goal_row = int(goal_position) // 10
        goal_column = int(goal_position) % 10

        if current_column < goal_column:
            if current_row > goal_row:
                for i in range(abs(goal_column - current_column)):
                    moves.append('1')
            else:
                for i in range(abs(goal_column - current_column)):
                    moves.append('5')
        else:
            if current_row > goal_row:
                for i in range(abs(goal_column - current_column)):
                    moves.append('7')
            else:
                for i in range(abs(goal_column - current_column)):
                    moves.append('3')

# turn magnet off

    moves.append('f')
    return moves


def magnet_to_current_position(goal_position, moves):
    global magnet_current_position

    current_row = int(magnet_current_position) // 10
    current_column = int(magnet_current_position) % 10

    goal_row = int(goal_position) // 10
    goal_column = int(goal_position) % 10

    # if the piece is moving forward
    if current_row > goal_row:
        for i in range(abs(goal_row - current_row)):
            moves.append('0')
    # if moving back
    else:
        for i in range(abs(current_row - goal_row)):
            moves.append('4')


    # if moving right
    if current_column < goal_column:
        for i in range(abs(goal_column - current_column)):
            moves.append('2')

    # if moving left
    else:
        for i in range(abs(current_column - goal_column)):
            moves.append('6')

    moves.append('9')


def physically_moving(best_moves, piece, ser):

    global magnet_current_position


    print (f"magnetpos: {magnet_current_position}")
    for i in range(len(best_moves)):
        moves = move(best_moves[i], piece)
        # 7 - forward and left
        # 0 - forward
        # 1 - forward and right
        # 2 - right
        # 5 - back and right
        # 4 - back
        # 3 - back and left
        # 6 - left
        for i in moves:
            if i == 'f':
                continue
            i = int(i)
            if i == 7:
                magnet_current_position = magnet_current_position - 11
            elif i == 0:
                magnet_current_position = magnet_current_position - 10
            elif i == 1:
                magnet_current_position = magnet_current_position - 9
            elif i == 2:
                magnet_current_position = magnet_current_position + 1
            elif i == 5:
                magnet_current_position = magnet_current_position + 11
            elif i == 4:
                magnet_current_position = magnet_current_position + 10
            elif i == 3:
                magnet_current_position = magnet_current_position + 9
            elif i == 6:
                magnet_current_position = magnet_current_position - 1

        print(moves)

        for i in moves:
            command = i
            ser.write(command.encode('utf-8'))
        time.sleep(5)

def calibrate(ser, camera):
    global magnet_current_position

    col = magnet_current_position % 10
    if col > 3:
        for i in range(col - 3):
            ser.write('6'.encode('utf-8'))
    if col < 3:
        for i in range(3 - col):
            ser.write('2'.encode('utf-8'))

    for i in range(int(7 - magnet_current_position // 10)):
        ser.write('4'.encode('utf-8'))
    detector = cv2.SimpleBlobDetector_create()
    lowerlimits = np.load(r"C:\Users\eppha\robootika\kaberobotkalev\BoardDetection\robotlowerlimits.npy")
    upperlimits = np.load(r"C:\Users\eppha\robootika\kaberobotkalev\BoardDetection\robotupperlimits.npy")
    x = False
    y = False
    while True:
        cbf = camera.current_chessboard_frame()

        frame = cbf.square_at(59)
        frame = frame.get_img()

        frame = cv2.inRange(frame, lowerlimits, upperlimits)
        frame = cv2.bitwise_not(frame)
        thresholded = cv2.rectangle(frame, (0, 0), (639, 29), (255, 255, 255), 2)

        keypoints = detector.detect(thresholded)
        if len(keypoints) < 1:
            continue

        frame_x = 30
        frame_y = 30

        magnet_x = keypoints[0].pt[0]
        magnet_y = keypoints[0].pt[1]

        print(magnet_x)
        print(magnet_y)
        if magnet_x < frame_x - 5:
            ser.write("d".encode("utf-8"))
        elif magnet_x > frame_x + 5:
            ser.write("a".encode("utf-8"))
        else:
            x = True
        if magnet_y < frame_y - 5:
            ser.write("s".encode("utf-8"))
        elif magnet_y > frame_y + 5:
            ser.write("w".encode("utf-8"))
        else:
            y = True
        time.sleep(0.5)
        if y and x:
            ser.write("0".encode("utf-8"))
            print("lopp")
            break

    magnet_current_position = 63
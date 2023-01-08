#!/usr/bin/python

import numpy as np

from gameplay import checkers
from gameplay import moving_the_pieces

# creating the two arrays current and next position will be stored in
current_state = np.array([[0 for col in range(8)] for row in range(8)])


# tagastab board state maatriksina
def board_array():
    f = open("./BoardDetection/board_array.txt", "r")
    x = f.read().strip()
    state = []
    row = []
    k = 0
    for i in x:
        row.append(i)
        if k == 7:
            k = 0
            state.append(row)
            row = []
        else:
            k += 1

    # from the perspective of the robot / camera
    # first number is the index counting top to bottom
    # second number is the index counting from left to right

    return state


def text_board(ser):
    global current_state

    # get the state of the board as a matrix
    current_state = board_array()

    current_board = checkers.Checkers(current_state)
    next_moves = current_board.get_next_move()

    moving_the_pieces.physically_moving(next_moves, current_board.get_piece(), ser)


if __name__ == "__main__":
    text_board()


def calibrate(ser,camera):
    moving_the_pieces.calibrate(ser,camera)

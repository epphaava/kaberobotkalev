#!/usr/bin/python

import gameplay.config as config
import gameplay.checkers as checkers

# tagastab board state maatriksina
def board_array():
    f = open("../BoardDetection/board_array.txt", "r")
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
    print(state)

    # maatriksi read on kaamera ülemisest ääres alumisse, paremalt vasakule

    return state

def text_board():

    # get the state of the board as a matrix
    config.current_state = board_array()

    current_board = checkers.Checkers(config.current_state)
    current_board.best_moves()

if __name__ == "__main__":
    text_board()

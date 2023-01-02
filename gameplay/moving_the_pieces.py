import math

import serial

# use this method to move the piece through corners to the given destination in best_moves

# this method assumes the removed pieces will be on the right side of the board

# from the perspective of the robot
# 0 - forward and left
# 1 - forward
# 2 - forward and right
# 3 - right
# 4 - back and right
# 5 - back
# 6 - back and left
# 7 - left

# 8 - magnet ON
# 9 - magnet OFF

magnet_current_position = 77


def move(best_moves, piece):
    global magnet_current_position

    moves = []

    if len(best_moves) == 0:
        print("no possible moves! game over :(")


    # if only one move to make
    elif len(best_moves) == 1 and piece == "regular":
        current_position = best_moves[0]['current_position']
        goal_position = best_moves[0]['goal_position']

        magnet_to_current_position(current_position, moves)

        current_row = current_position
        current_column = current_position % 10

        goal_row = goal_position
        goal_column = goal_position % 10

        # if the piece is moving forward
        if current_row < goal_row:
            if current_column < goal_column:
                for i in range(goal_column - current_column):
                    moves.append('2')
            else:
                for i in range(current_column - goal_column):
                    moves.append('0')

        # if moving back (possible if it is a crown)
        else:
            if current_column < goal_column:
                for i in range(goal_column - current_column):
                    moves.append('4')
            else:
                for i in range(current_column - goal_column):
                    moves.append('6')

    # if there is more than one move to make
    elif len(best_moves) >= 1 and piece == "regular":
        for move_nr in range(len(best_moves)):

            current_position = best_moves[move_nr]['current_position']
            goal_position = best_moves[move_nr]['goal_position']

            magnet_to_current_position(current_position, moves)

            if goal_position == "*crown" or goal_position == "*remove":
                # switch regular piece for a crown or remove a piece
                # in both cases the piece needs to be moved off the board
                # currently the crown has to be added by hand as we don't know where we could keep the crown pieces
                moves.append('3')
                for i in range(math.ceil((7 - current_position % 10) / 2)):
                    moves.append('2')
                    moves.append('4')
            else:
                # if it makes to this condition there are two possibilities
                # one move for crowning
                # or two moves to remove the opponent's piece

                current_row = current_position
                current_column = current_position % 10

                goal_row = goal_position
                goal_column = goal_position % 10

                # if the piece is moving forward
                if current_row < goal_row:
                    if current_column < goal_column:
                        for i in range(goal_column - current_column):
                            moves.append('2')
                    else:
                        for i in range(current_column - goal_column):
                            moves.append('0')

                # if moving back (possible if it is a crown)
                else:
                    if current_column < goal_column:
                        for i in range(goal_column - current_column):
                            moves.append('4')
                    else:
                        for i in range(current_column - goal_column):
                            moves.append('6')
        # turn magnet off
        moves.append('9')
        return moves


def magnet_to_current_position(goal_position, moves):
    global magnet_current_position

    current_row = magnet_current_position
    current_column = magnet_current_position % 10

    goal_row = goal_position
    goal_column = goal_position % 10

    # if the piece is moving forward
    if current_row < goal_row:
        for i in range(goal_row - current_row):
            moves.append('1')
    # if moving back
    else:
        for i in range(current_row - goal_row):
            moves.append('5')

    # if moving right
    if current_column < goal_column:
        for i in range(goal_column - current_column):
            moves.append('3')

    # if moving left
    else:
        for i in range(current_column - goal_column):
            moves.append('7')

    moves.append('8')


def physically_moving(best_moves, piece):
    baudRate = 9600
    ser = serial.Serial("COM4", baudRate)
    moves = move(best_moves, piece)

    for i in moves:
        command = i
        ser.write(command.encode('utf-8'))
    ser.close()

import math

import serial

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

magnet_current_position = 70


def move(best_moves, piece):
    global magnet_current_position

    moves = []

    if len(best_moves) == 0:
        print("no possible moves! game over :(")


    # if only one move to make
    elif len(best_moves) == 1 and piece == "regular":
        current_position = int(best_moves[0]['current_position'])
        goal_position = best_moves[0]['goal_position']

        magnet_to_current_position(current_position, moves)

        current_row = int(current_position) // 10
        current_column = int(current_position) % 10

        goal_row = int(goal_position) // 10
        goal_column = int(goal_position) % 10

        # if the piece is moving forward
        if current_row > goal_row:
            if current_column < goal_column:
                for i in range(abs(goal_column - current_column)):
                    moves.append('1')
            else:
                for i in range(abs(current_column - goal_column)):
                    moves.append('7')


        # if moving back (possible if it is a crown)
        else:
            if current_column > goal_column:
                for i in range(abs(goal_column - current_column)):
                    moves.append('5')
            else:
                for i in range(abs(current_column - goal_column)):
                    moves.append('3')

    # if there is more than one move to make
    elif len(best_moves) >= 2 and piece == "regular":
        for move_nr in range(len(best_moves)):

            current_position = int(best_moves[move_nr]['current_position'])
            goal_position = best_moves[move_nr]['goal_position']

            print(current_position)
            print("moving piece to current")
            magnet_to_current_position(current_position, moves)

            if goal_position == "*crown" or goal_position == "*remove":
                # switch regular piece for a crown or remove a piece
                # in both cases the piece needs to be moved off the board
                # currently the crown has to be added by hand as we don't know where we could keep the crown pieces
                moves.append('2')
                magnet_current_position = magnet_current_position + 1
                for i in range(math.ceil((7 - current_position % 10) / 2)):
                    moves.append('1')
                    magnet_current_position = magnet_current_position - 9

                    moves.append('7')
                    magnet_current_position = magnet_current_position - 11

                print("current. ", magnet_current_position )
                moves.append('8')


            else:
                # if it makes to this condition there are two possibilities
                # one move for crowning
                # or two moves to remove the opponent's piece

                current_row = int(current_position) // 10
                current_column = int(current_position) % 10

                goal_row = int(goal_position) // 10
                goal_column = int(goal_position) % 10

                # if the piece is moving forward
                if current_row > goal_row:
                    if current_column > goal_column:
                        for i in range(abs(goal_column - current_column)):
                            moves.append('1')
                    else:
                        for i in range(abs(current_column - goal_column)):
                            moves.append('7')

                # if moving back (possible if it is a crown)
                else:
                    if current_column > goal_column:
                        for i in range(abs(goal_column - current_column)):
                            moves.append('5')
                    else:
                        for i in range(abs(current_column - goal_column)):
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


def physically_moving(best_moves, piece):
    #baudRate = 9600
    #ser = serial.Serial("COM5", baudRate)
    global magnet_current_position


    print (f"magnetpos: {magnet_current_position}" )
    moves = move(best_moves, piece)
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

    #for i in moves:
    #    command = i
    #    ser.write(command.encode('utf-8'))
    #ser.close()

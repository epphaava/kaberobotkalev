
# IT IS ENTIRELY POSSIBLE I AM MAKING THIS WAYY TOO COMPLICATED

# use this method to move the piece through corners to the given destination in best_moves

# dictionary with the corners of black squares
black_corners = {}
# dictionary with the corners of white squares
white_corners = {}

# {00: {right_top: xxx, left_top: yyy, right_bottom: zzz, left_bottom: www}}

def move(best_moves, piece):
    global black_corners
    global white_corners

    if len(best_moves) == 0:
        print("no possible moves! game over :(")

    elif len(best_moves) == 1 and piece == "regular":
        current_position = best_moves[0]['current_position']
        goal_position = best_moves[0]['goal_position']
        if black_corners[current_position]['right_top'] == black_corners[goal_position]['left_bottom']:
            # move through that corner to the next square until piece is detected by the camera at the goal position
            return
        elif black_corners[current_position]['left_top'] == black_corners[goal_position]['right_bottom']:
            # move through that corner to the next square until piece is detected by the camera at the goal position
            return

    elif len(best_moves) >= 1 and piece == "regular":
        for move_nr in range(len(best_moves)):
            current_position = best_moves[move_nr]['current_position']
            goal_position = best_moves[move_nr]['goal_position']

            if goal_position == "*crown":
                # switch regular piece for a crown
                return
            elif goal_position == "*remove":
                # move to for example white_corners[current_position]['left_top']
                # the corner depend on where we decide to move removed pieces and where exactly the current position is
                # from there in a diagonal through white squares to the side of the table
                return
            else:
                # if it makes to this condition there are two possibilities
                # one move for crowning
                # or two moves to remove the opponent's piece

                if current_position < goal_position:
                    # this means we are moving backwards on the board
                    forward = False
                else:
                    forward = True

                if current_position // 10 < goal_position // 10:
                    # this means we are moving to the right side of the board
                    right = True
                else:
                    right = False



                return



if __name__ == "__main__":
    move([], "regular")

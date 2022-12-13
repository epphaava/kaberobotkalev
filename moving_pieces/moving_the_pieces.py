
# IT IS ENTIRELY POSSIBLE I AM MAKING THIS WAYY TOO COMPLICATED

# use this method to move the piece through corners to the given destination in best_moves

def move(best_moves, piece):

    if len(best_moves) == 0:
        print("no possible moves! game over :(")

    # if only one move to make
    elif len(best_moves) == 1 and piece == "regular":
        current_position = best_moves[0]['current_position']
        goal_position = best_moves[0]['goal_position']

        # current -> goal

    # if there is more than one move to make
    elif len(best_moves) >= 1 and piece == "regular":
        for move_nr in range(len(best_moves)):
            current_position = best_moves[move_nr]['current_position']
            goal_position = best_moves[move_nr]['goal_position']

            if goal_position == "*crown":
                # switch regular piece for a crown
                return
            elif goal_position == "*remove":
                # move to a white square next to current location
                # depending on where the location is and where the removed pieces will go the piece will move in the whitee diagonal to be removed
                return
            else:
                # if it makes to this condition there are two possibilities
                # one move for crowning
                # or two moves to remove the opponent's piece

                # current -> goal
                return

        return

if __name__ == "__main__":
    move([], "regular")

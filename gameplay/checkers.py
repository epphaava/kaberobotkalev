# https://github.com/Dandoko/quba_robotic_arm/blob/master/computer-vision/checkers.py

import json
import os


class Checkers:

    def __init__(self, board):
        self.size = 8
        self.board = board
        self.longest_chain = 0
        self.chain_moves = []
        self.best_moves = []
        self.best_priority_score = 0
        self.piece = "regular"

    def get_piece(self):
        return self.piece

    # get the current position of the piece and the goal position where it should be moved
    def get_next_move(self):
        for x in range(self.size):
            for y in range(self.size):

                # the pieces on the board:
                # robot: "x" for regular pieces, "y" for crowns
                # opponent: "o" for regular pieces, "p" for crowns
                if self.board[x][y] == 'x':
                    self.get_priority(x, y, False)
                elif self.board[x][y] == 'y':
                    self.get_priority(x, y, True)
        file_num = 1
        if not os.path.isdir("./moves"):
            try:
                os.mkdir("./moves")
            except OSError:
                print("Directory creation failed")

        while os.path.isfile("./moves/" + str(file_num) + ".json"):
            file_num += 1
        print("move nr. ", file_num)
        for x in range(len(self.best_moves)):
            with open('./moves/' + str(file_num + x) + ".json", 'w') as outfile:
                json.dump(self.best_moves[x], outfile)

        print("best moves: ", self.best_moves)

        print(
            "Kasutaja poolt vaadatuna:\nEsimene number on vasakult kaamera poole loetuna 0-7, \nTeine number on paremalt vasakule loetuna 0-7")
        return self.best_moves

    def get_priority(self, x, y, is_crown):

        # if it is not a crown
        if not is_crown:
            capture_priority = 1
            top_left_priority = 1
            top_right_priority = 1

            # will make the best turn choice according to the priority score:
            # capture chain = 10*n
            # crowning = 29
            # keeping a line = 1 * n
            # safe moves

            # find the longest chain of captures
            captures = self.captures(x, y)
            if len(captures) > 0:
                capture_priority *= len(captures) * 10
                best_move = capture_priority
            else:
                # find the longest diagonal of gamepieces
                if self.is_position(x - 1, y - 1) and self.board[x - 1][y - 1] == '-':
                    top_left_priority += self.longest_line(x - 1, y - 1)
                if self.is_position(x - 1, y + 1) and self.board[x - 1][y + 1] == '-':
                    top_right_priority += self.longest_line(x - 1, y + 1)

                # crown
                if self.is_position(x - 1, y - 1) and self.board[x - 1][y - 1] == '-' and x == 1:
                    top_left_priority += 29
                if self.is_position(x - 1, y + 1) and self.board[x - 1][y + 1] == '-' and x == 1:
                    top_right_priority += 29

                # which way is it safe to move
                if self.is_position(x - 1, y - 1) and self.board[x - 1][y - 1] == '-' and self.is_safe(x - 1, y - 1, x,
                                                                                                       y):
                    top_left_priority += 3
                if self.is_position(x - 1, y + 1) and self.board[x - 1][y + 1] == '-' and self.is_safe(x - 1, y + 1, x,
                                                                                                       y):
                    top_right_priority += 3

                # give priority to middle of board moves
                if self.is_position(x - 1, y - 1) and self.board[x - 1][y - 1] == '-' and 2 < y < 5:
                    top_left_priority += 1
                if self.is_position(x - 1, y + 1) and self.board[x - 1][y + 1] == '-' and 2 < y < 5:
                    top_right_priority += 1

                best_move = max(top_left_priority, top_right_priority)

            if best_move == capture_priority and best_move > self.best_priority_score:
                self.best_moves = captures
                self.best_priority_score = capture_priority
                self.piece = "regular"

            elif best_move == top_left_priority and best_move > self.best_priority_score:
                self.best_moves = [{"current_position": str(x) + str(y), "goal_position": str(x - 1) + str(y - 1)}]
                if x == 1: self.best_moves.append(
                    {"current_position": str(x - 1) + str(y - 1), "goal_position": "*crown"})
                self.best_priority_score = top_left_priority
                self.piece = "regular"

            elif best_move == top_right_priority and best_move > self.best_priority_score:
                self.best_moves = [{"current_position": str(x) + str(y), "goal_position": str(x - 1) + str(y + 1)}]
                if x == 1: self.best_moves.append(
                    {"current_position": str(x - 1) + str(y + 1), "goal_position": "*crown"})
                self.best_priority_score = top_right_priority
                self.piece = "regular"

        # if it is a crown
        else:
            capture_priority = 1
            top_left_priority = [1, 8, 8]
            top_right_priority = [1, 8, 8]
            bottom_left_priority = [1, 8, 8]
            bottom_right_priority = [1, 8, 8]

            captures = self.crown_captures(x, y, [])
            if len(captures[0]) > 0:
                capture_priority *= len(captures[0]) * 10 - captures[1]
                best_move = capture_priority
            else:
                # give priority to safe moves
                i = 1
                while True:
                    if self.is_position(x - i, y - i) and self.board[x - i][y - i] == '-' and self.is_safe(x - i, y - i,
                                                                                                           x - i + 1,
                                                                                                           y - i + 1):
                        top_left_priority[0] += 3
                        top_left_priority[1] = x - i
                        top_left_priority[2] = y - i
                        break
                    if self.is_position(x - i, y + i) and self.board[x - i][y + i] == '-' and self.is_safe(x - i, y - i,
                                                                                                           x - i + 1,
                                                                                                           y - i - 1):
                        top_right_priority[0] += 3
                        top_right_priority[1] = x - i
                        top_right_priority[2] = x + i
                        break

                    if self.is_position(x + i, y + i) and self.board[x + i][y + i] == '-' and self.is_safe(x + i, y + i,
                                                                                                           x + i - 1,
                                                                                                           y + i - 1):
                        bottom_left_priority[1] = x + i
                        bottom_left_priority[2] = x + i
                        bottom_left_priority[0] += 3
                        break

                    if self.is_position(x + i, y - i) and self.board[x + i][y - i] == '-' and self.is_safe(x + i, y + i,
                                                                                                           x + i - 1,
                                                                                                           y + i + 1):
                        bottom_right_priority[1] = x - i
                        bottom_right_priority[2] = x + i
                        bottom_right_priority[0] += 3
                        break
                    i += 1

                best_move = max(top_left_priority[0], top_right_priority[0], bottom_right_priority[0],
                                bottom_left_priority[0])

            if best_move == capture_priority and best_move > self.best_priority_score:
                self.best_moves = captures[0]
                self.best_priority_score = capture_priority
                self.piece = "crown"

            elif best_move == top_left_priority[0] and best_move > self.best_priority_score:
                self.best_moves = [{"current_position": str(x) + str(y),
                                    "goal_position": str(top_left_priority[1]) + str(top_right_priority[1])}]
                self.best_priority_score = top_left_priority[0]
                self.piece = "crown"

            elif best_move == top_right_priority[0] and best_move > self.best_priority_score:
                self.best_moves = [{"current_position": str(x) + str(y),
                                    "goal_position": str(top_right_priority[1]) + str(top_right_priority[2])}]
                self.best_priority_score = top_right_priority[0]
                self.piece = "crown"

        return self.best_moves

    # is it safe to move to (x, y)
    def is_safe(self, x, y, prev_x, prev_y):
        if (self.is_position(x - 1, y - 1) and self.board[x - 1][y - 1] == 'o' and self.is_position(x + 1, y + 1) and (
                self.board[x + 1][y + 1] == '-' or (x + 1 == prev_x and y + 1 == prev_y))):
            return False
        if (self.is_position(x - 1, y + 1) and self.board[x - 1][y + 1] == 'o' and self.is_position(x + 1, y - 1) and (
                self.board[x + 1][y - 1] == '-' or (x + 1 == prev_x and y - 1 == prev_y))):
            return False
        if (self.is_position(x + 1, y + 1) and self.board[x + 1][y + 1] == 'o' and self.is_position(x - 1, y - 1) and (
                self.board[x - 1][y - 1] == '-' or (x - 1 == prev_x and y - 1 == prev_y))):
            return False
        if (self.is_position(x + 1, y - 1) and self.board[x + 1][y - 1] == 'o' and self.is_position(x - 1, y + 1) and (
                self.board[x - 1][y + 1] == '-' or (x - 1 == prev_x and y + 1 == prev_y))):
            return False

        i = 1
        while self.is_position(x - i, y - i) and self.is_position(x + 1, y + 1):
            if self.board[x - i][y - i] == 'p' and (self.board[x + 1][y + 1] == '-' or (x + 1 == prev_x and y + 1 ==
                                                                                        prev_y)):
                return False
            i += 1

        i = 1
        while self.is_position(x - i, y + i) and self.is_position(x + 1, y - 1):
            if self.board[x - i][y + i] == 'p' and (self.board[x + 1][y - 1] == '-' or (x + 1 == prev_x and y - 1 ==
                                                                                        prev_y)):
                return False
            i += 1
        return True

    # longes diagonal of the pieces
    def longest_line(self, x, y):
        longest_left_to_right = 0
        longest_right_to_left = 0
        pos_x = x
        pos_y = y

        # top left to bottom right divided into two

        # center to top left
        while self.is_position(pos_x - 1, pos_y - 1) and self.board[pos_x - 1][pos_y - 1] == 'x':
            longest_left_to_right += 1
            pos_x -= 1
            pos_y -= 1
        pos_x = x
        pos_y = y

        # center to bottom right
        while self.is_position(pos_x + 1, pos_y + 1) and self.board[pos_x + 1][pos_y + 1] == 'x':
            longest_left_to_right += 1
            pos_x += 1
            pos_y += 1
        pos_x = x
        pos_y = y

        # top right to bottom left divided into two

        # center to top right
        while self.is_position(pos_x - 1, pos_y + 1) and self.board[pos_x - 1][pos_y + 1] == 'x':
            longest_right_to_left += 1
            pos_x -= 1
            pos_y += 1
        pos_x = x
        pos_y = y

        # center to bottom left
        while self.is_position(pos_x + 1, pos_y - 1) and self.board[pos_x + 1][pos_y - 1] == 'x':
            longest_right_to_left += 1
            pos_x += 1
            pos_y -= 1

        return max(longest_left_to_right, longest_right_to_left)

    # does (x, y) exist on the board?
    def is_position(self, x, y):
        if 0 <= x < self.size and 0 <= y < self.size:
            return True
        return False

    # is it possible to capture the opponent's piece in the given direction? (with a regular piece)
    def can_capture(self, x, y, direction):
        if direction == "top left":
            if (self.is_position(x - 1, y - 1) and self.is_position(x - 2, y - 2) and (self.board[x - 1][
                                                                                           y - 1] == 'o' or
                                                                                       self.board[x - 1][
                                                                                           y - 1] == 'p') and
                    self.board[x - 2][y - 2] == '-'):
                return True
        elif direction == "top right":
            if (self.is_position(x - 1, y + 1) and self.is_position(x - 2, y + 2) and (self.board[x - 1][
                                                                                           y + 1] == 'o' or
                                                                                       self.board[x - 1][
                                                                                           y + 1] == 'p') and
                    self.board[x - 2][y + 2] == '-'):
                return True
        elif direction == "bottom left":
            return False

            # in this game it is not allowed for a regular piece to remove a piece moving back
            if (self.is_position(x + 1, y + 1) and self.is_position(x + 2, y + 2) and (self.board[x + 1][
                                                                                           y + 1] == 'o' or
                                                                                       self.board[x + 1][
                                                                                           y + 1] == 'p') and
                    self.board[x + 2][y + 2] == '-'):
                return True
        elif direction == "bottom right":
            return False
            if (self.is_position(x + 1, y - 1) and self.is_position(x + 2, y - 2) and (self.board[x + 1][
                                                                                           y - 1] == 'o' or
                                                                                       self.board[x + 1][
                                                                                           y - 1] == 'p') and
                    self.board[x + 2][y - 2] == '-'):
                return True
        return False

    # in which direction is it possible to capture pieces and how many at once (with a regular piece)
    def captures(self, x, y, moves=None):

        # base - cannot capture anything
        if moves is None:
            moves = [0, []]
        if not self.can_capture(x, y, "top left") and not self.can_capture(x, y, "top right") and not self.can_capture(
                x, y, "bottom right") and not self.can_capture(x, y, "bottom right"):
            if moves[0] > self.longest_chain:
                self.longest_chain = moves[0]
                self.chain_moves = moves[1]
            return self.chain_moves

        if self.can_capture(x, y, "top left"):
            self.captures(x - 2, y - 2, [moves[0] + 1, moves[1] + [
                {"current_position": str(x - 1) + str(y - 1),
                 "goal_position": "*remove"}] + [
                                             {"current_position": str(x) + str(y),
                                              "goal_position": str(x - 2) + str(y - 2)}]])

        if self.can_capture(x, y, "top right"):
            self.captures(x - 2, y + 2, [moves[0] + 1, moves[1] + [{"current_position": str(x - 1) + str(y + 1),
                                                                    "goal_position": "*remove"}] + [
                                             {"current_position": str(x) + str(y),
                                              "goal_position": str(x - 2) + str(y + 2)}]])

        if self.can_capture(x, y, "bottom left"):
            self.captures(x + 2, y + 2, [moves[0] + 1, moves[1] + [{"current_position": str(x + 1) + str(y + 1),
                                                                    "goal_position": "*remove"}] + [
                                             {"current_position": str(x) + str(y),
                                              "goal_position": str(x + 2) + str(y + 2)}]])

        if self.can_capture(x, y, "bottom right"):
            self.captures(x + 2, y - 2, [moves[0] + 1, moves[1] + [
                {"current_position": str(x + 1) + str(y - 1),
                 "goal_position": "*remove"}] + [{"current_position": str(x) + str(y),
                                                  "goal_position": str(x + 2) + str(y - 2)}]])

        return self.chain_moves

    # is it possible to capture the opponent's piece in the given direction? (with a crown)
    def crown_can_capture(self, x, y, direction, already_captured):

        variable = 1
        if direction == "top left":
            while self.is_position(x - variable, y - variable) and self.is_position(x - variable - 1, y - variable - 1):
                allowed = True
                if self.board[x - variable][y - variable] == 'o' and self.board[x - variable - 1][
                    y - variable - 1] == '-':
                    for i in already_captured:
                        if i[0] == x - variable and i[1] == y - variable:
                            allowed = False
                            break
                    if allowed:
                        already_captured.append([x - variable, y - variable])
                        return [True, x - variable - 1, y - variable - 1, already_captured]
                variable += 1
        elif direction == "top right":
            while self.is_position(x - variable, y + variable) and self.is_position(x - variable - 1, y + variable + 1):
                allowed = True
                if self.board[x - variable][y + variable] == 'o' and self.board[x - variable - 1][
                    y + variable + 1] == '-':
                    for i in already_captured:
                        if i[0] == x - variable and i[1] == y + variable:
                            allowed = False
                            break
                    if allowed:
                        already_captured.append([x - variable, y + variable])
                        return [True, x - variable - 1, y + variable + 1, already_captured]
                variable += 1
        elif direction == "bottom left":
            while self.is_position(x + variable, y + variable) and self.is_position(x + variable + 1, y + variable + 1):
                allowed = True
                if self.board[x + variable][y + variable] == 'o' and self.board[x + variable + 1][
                    y + variable + 1] == '-':
                    for i in already_captured:
                        if i[0] == x + 1 and i[1] == y + 1:
                            allowed = False
                            break
                    if allowed:
                        already_captured.append([x + variable, y + variable])
                        return [True, x + variable + 1, y + variable + 1, already_captured]
                variable += 1
        elif direction == "bottom right":
            while self.is_position(x + variable, y - variable) and self.is_position(x + variable + 1, y - variable - 1):
                allowed = True
                if self.board[x + variable][y - variable] == 'o' and self.board[x + variable + 1][
                    y - variable - 1] == '-':
                    for i in already_captured:
                        if i[0] == x + 1 and i[1] == y - 1:
                            allowed = False
                            break
                    if allowed:
                        already_captured.append([x + variable, y - variable])
                        return [True, x + variable + 1, y - variable - 1, already_captured]
                variable += 1
        return [False]

    # in which direction is it possible to capture pieces and how many at once (with a crown)
    def crown_captures(self, x, y, already_captured, moves=None):

        if moves is None:
            moves = [0, []]
        top_left_capture = self.crown_can_capture(x, y, "top left", already_captured)
        top_right_capture = self.crown_can_capture(x, y, "top right", already_captured)
        bottom_left_capture = self.crown_can_capture(x, y, "bottom left", already_captured)
        bottom_right_capture = self.crown_can_capture(x, y, "bottom right", already_captured)

        safety = 0

        # base - cannot capture anything
        if not top_left_capture[0] and not top_right_capture[0] and not bottom_right_capture[0] and not \
                bottom_left_capture[0]:
            self.longest_chain = moves[0]
            self.chain_moves = moves[1]
            return [self.chain_moves, safety]

        if top_left_capture[0]:
            x_left = top_left_capture[1]
            y_left = top_left_capture[2]

            self.crown_captures(x_left, y_left, already_captured, [moves[0] + 1, moves[1] + [
                {"current_position": str(x) + str(y), "goal_position": str(x_left) + str(y_left)}] + [
                                                                       {"current_position": str(x_left + 1) + str(
                                                                           y_left + 1),
                                                                        "goal_position": "*remove"}]])
            if not self.is_safe(top_left_capture[1], top_left_capture[2], top_left_capture[1] + 1,
                                top_left_capture[2] + 1):
                safety = 3

        if top_right_capture[0]:
            x_right = top_right_capture[1]
            y_right = top_right_capture[2]

            self.crown_captures(x_right, y_right, already_captured, [moves[0] + 1, moves[1] + [
                {"current_position": str(x) + str(y), "goal_position": str(x_right) + str(y_right)}] + [
                                                                         {"current_position": str(x_right + 1) + str(
                                                                             y_right - 1),
                                                                          "goal_position": "*remove"}]])
            if not self.is_safe(top_right_capture[1], top_right_capture[2], top_right_capture[1] + 1,
                                top_right_capture[2] - 1):
                safety = 3

        if bottom_left_capture[0]:
            bottom_x_left = bottom_left_capture[1]
            bottom_y_left = bottom_left_capture[2]

            self.crown_captures(bottom_x_left, bottom_y_left, already_captured, [moves[0] + 1, moves[1] + [
                {"current_position": str(bottom_x_left - 1) + str(bottom_y_left - 1), "goal_position": "*remove"}]] + [
                                    {"current_position": str(x) + str(y),
                                     "goal_position": str(bottom_x_left) + str(bottom_y_left)}])
            if not self.is_safe(bottom_left_capture[1], bottom_left_capture[2], bottom_left_capture[1] + 1,
                                bottom_left_capture[2] + 1):
                safety = 3

        if bottom_right_capture[0]:
            bottom_x_right = bottom_right_capture[1]
            bottom_y_right = bottom_right_capture[2]

            self.crown_captures(bottom_x_right, bottom_y_right, already_captured, [moves[0] + 1, moves[1] + [
                {"current_position": str(bottom_x_right - 1) + str(bottom_y_right + 1), "goal_position": "*remove"}]
                                                                                   + [{"current_position": str(x) + str(
                y), "goal_position": str(bottom_x_right) + str(bottom_y_right)}]])
            if not self.is_safe(bottom_right_capture[1], bottom_right_capture[2], bottom_right_capture[1] + 1,
                                bottom_right_capture[2] - 1):
                safety = 3

        return [self.chain_moves, safety]

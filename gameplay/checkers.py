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

    # get the current position of the piece and the goal position where it should be moved
    def get_next_move(self):
        for x in range(self.size):
            for y in range(self.size):

                # boardil märgitud roboti nupud "x" ja "y" ning vastase nupud "o" ja "p"
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
        print(file_num)
        for x in range(len(self.best_moves)):
            with open('./moves/' + str(file_num + x) + ".json", 'w') as outfile:
                json.dump(self.best_moves[x], outfile)

        print("best moves: ", self.best_moves)
        return self.best_moves

    def get_priority(self, x, y, is_crown):
        # kui tegemist tavalise nupuga
        if not is_crown:
            capture_priority = 1
            top_left_priority = 1
            top_right_priority = 1

            # hiljem valime priority score järgi:
            # capture chain = 10*n
            # crowning = 29 (kui kunagi otsustame seda teha)
            # keeping a line = 1 * n
            # safe moves

            # leiame pikim käikude järjestuse
            captures = self.captures(x, y)
            if len(captures) > 0:
                capture_priority *= len(captures) * 10

            # leiame pikima nuppudest koosneva diagonaali
            if self.is_position(x - 1, y - 1) and self.board[x - 1][y - 1] == '-':
                top_left_priority += self.longest_line(x - 1, y - 1)
            if self.is_position(x - 1, y + 1) and self.board[x - 1][y + 1] == '-':
                top_right_priority += self.longest_line(x - 1, y + 1)

            # tammiks saamine
            if self.is_position(x - 1, y - 1) and self.board[x - 1][y - 1] == 0 and x == 1:
                top_left_priority += 29
            if self.is_position(x - 1, y + 1) and self.board[x - 1][y + 1] == 0 and x == 1:
                top_right_priority += 29

            # kuhu poole on safe liikuda, ei sööda ära
            if self.is_position(x - 1, y - 1) and self.board[x - 1][y - 1] == '-' and self.is_safe(x - 1, y - 1, x, y):
                top_left_priority += 3
            if self.is_position(x - 1, y + 1) and self.board[x - 1][y + 1] == '-' and self.is_safe(x - 1, y + 1, x, y):
                top_right_priority += 3

            # give priority to middle of board moves
            if self.is_position(x - 1, y - 1) and self.board[x - 1][y - 1] == '-' and 2 < y < 5:
                top_left_priority += 1
            if self.is_position(x - 1, y + 1) and self.board[x - 1][y + 1] == '-' and 2 < y < 5:
                top_right_priority += 1

            best_move = max(capture_priority, top_left_priority, top_right_priority)

            # kui söömiste punktid paremad kui ükski priority score
            if best_move == capture_priority and best_move > self.best_priority_score:
                # siis captured on kõige parem järgmine käik
                self.best_moves = captures
                self.best_priority_score = capture_priority

            # kui mõistlik liikuda vasakule
            elif best_move == top_left_priority and best_move > self.best_priority_score:
                self.best_moves = [{"current_position": str(x) + str(y), "goal_position": str(x - 1) + str(y - 1)}]
                if x == 1: self.best_moves.append(
                    {"current_position": str(x - 1) + str(y - 1), "goal_position": "*crown"})
                self.best_priority_score = top_left_priority

            # kui mõistlik liikuda paremale
            elif best_move == top_right_priority and best_move > self.best_priority_score:
                self.best_moves = [{"current_position": str(x) + str(y), "goal_position": str(x - 1) + str(y + 1)}]
                if x == 1: self.best_moves.append(
                    {"current_position": str(x - 1) + str(y + 1), "goal_position": "*crown"})
                self.best_priority_score = top_right_priority

        # kui tegemist tammiga
        else:
            capture_priority = 1
            top_left_priority = [1]
            top_right_priority = [1]

            captures = self.crown_captures(x, y)
            if len(captures[0]) > 0:
                capture_priority *= len(captures[0]) * 10 - captures[1]

            # give priority to safe moves
            i = 1
            while True:
                if self.is_position(x - i, y - i) and self.board[x - i][y - i] == '-' and self.is_safe(x - i, y - i,
                                                                                                       x - i + 1,
                                                                                                       y - i + 1):
                    top_left_priority += 3
                    top_left_priority.append(x - i)
                    top_left_priority.append(y - i)
                    break
                if self.is_position(x - i, y + i) and self.board[x - i][y + i] == '-' and self.is_safe(x - i, y - i,
                                                                                                       x - i + 1,
                                                                                                       y - i - 1):
                    top_right_priority.append(x - i)
                    top_right_priority.append(x + 1)
                    top_left_priority += 3
                    break

            # valime mis siis parim edasine tegevus
            best_move = max(capture_priority, top_left_priority[0], top_right_priority[0])

            # kui söömiste punktid paremad kui ükski priority score
            if best_move == capture_priority and best_move > self.best_priority_score:
                # siis captured on kõige parem järgmine käik
                self.best_moves = captures[0]
                self.best_priority_score = capture_priority

            # kui mõistlik liikuda vasakule
            elif best_move == top_left_priority[0] and best_move > self.best_priority_score:
                self.best_moves = [{"current_position": str(x) + str(y),
                                    "goal_position": str(top_left_priority[1]) + str(top_right_priority[1])}]
                self.best_priority_score = top_left_priority[0]

            # kui mõistlik liikuda paremale
            elif best_move == top_right_priority[0] and best_move > self.best_priority_score:
                self.best_moves = [{"current_position": str(x) + str(y),
                                    "goal_position": str(top_right_priority[1]) + str(top_right_priority[2])}]
                self.best_priority_score = top_right_priority[0]

        return self.best_moves

    # kui käia kohale (x,y), kas see on safe move
    def is_safe(self, x, y, prev_x, prev_y):
        if (self.is_position(x - 1, y - 1) and self.board[x - 1][y - 1] == 'o' and self.is_position(x + 1, y + 1) and (
                self.board[x + 1][y + 1] == '-' or (x + 1 == prev_x and y + 1 == prev_y))):
            return False
        if (self.is_position(x - 1, y + 1) and self.board[x - 1][y + 1] == 'o' and self.is_position(x + 1, y - 1) and (
                self.board[x + 1][y - 1] == '-' or (x + 1 == prev_x and y - 1 == prev_y))):
            return False

        i = 1
        while self.is_position(x - i, y - i) and self.is_position(x + 1, y + 1):
            if self.board[x - i][y - i] == 'p' and (self.board[x + 1][y + 1] == '-' or (x + 1 == prev_x and y + 1 ==
                                                                                        prev_y)):
                return False

        i = 1
        while self.is_position(x - i, y + i) and self.is_position(x + 1, y - 1):
            if self.board[x - i][y + i] == 'p' and (self.board[x + 1][y - 1] == '-' or (x + 1 == prev_x and y - 1 ==
                                                                                        prev_y)):
                return False
        return True

    # pikim roboti nuppude rida (diagonaal)
    def longest_line(self, x, y):
        longest_left_to_right = 0
        longest_right_to_left = 0
        pos_x = x
        pos_y = y

        # top left to bottom right jagatud kaheks

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

        # top right to bottom left jagatud kaheks

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

    # kas antud positsioon eksisteerib laual?
    def is_position(self, x, y):
        if 0 <= x < self.size and 0 <= y < self.size:
            return True
        return False

    # kas saab etteantud suunas nuppu võtta?
    def can_capture(self, x, y, direction):
        if direction == "top left":
            if (self.is_position(x - 1, y - 1) and self.is_position(x - 2, y - 2) and self.board[x - 1][
                y - 1] == 'o' and
                    self.board[x - 2][y - 2] == '-'):
                return True
        elif direction == "top right":
            if (self.is_position(x - 1, y + 1) and self.is_position(x - 2, y + 2) and self.board[x - 1][
                y + 1] == 'o' and
                    self.board[x - 2][y + 2] == '-'):
                return True
        return False

    # kuhu liikudes saab süüa vastase nuppe (ja kui mitu järjest)
    def captures(self, x, y, moves=None):

        # baas - ei saa süüa midagi
        if moves is None:
            moves = [0, []]
        if not self.can_capture(x, y, "top left") and not self.can_capture(x, y, "top right"):
            if moves[0] > self.longest_chain:
                self.longest_chain = moves[0]
                self.chain_moves = moves[1]
            return self.chain_moves

        # kui saab liikuda mõlemale poole
        if self.can_capture(x, y, "top left") and self.can_capture(x, y, "top right"):

            # vaatab kui palju saaks vasakule minnes võtta
            # märgib, millisel positsioonil liigutatav nupp ja kuhu selle liigutama peab (kui minna selle käiguga)
            self.captures(x - 2, y - 2, [moves[0] + 1, moves[1] + [
                {"current_position": str(x) + str(y), "goal_position": str(x - 2) + str(y - 2)}] + [
                                             {"current_position": str(x - 1) + str(y - 1),
                                              "goal_position": "*remove"}]])
            # kui palju saaks paremale minnes võtta
            self.captures(x - 2, y + 2, [moves[0] + 1, moves[1] + [
                {"current_position": str(x) + str(y), "goal_position": str(x - 2) + str(y + 2)}] + [
                                             {"current_position": str(x - 1) + str(y + 1),
                                              "goal_position": "*remove"}]])

        # vaatleme ainult vasakule võtmist
        elif self.can_capture(x, y, "top left"):
            self.captures(x - 2, y - 2, [moves[0] + 1, moves[1] + [
                {"current_position": str(x) + str(y), "goal_position": str(x - 2) + str(y - 2)}] + [
                                             {"current_position": str(x - 1) + str(y - 1),
                                              "goal_position": "*remove"}]])

        # ainult paremale võtmist
        elif self.can_capture(x, y, "top right"):
            self.captures(x - 2, y + 2, [moves[0] + 1, moves[1] + [
                {"current_position": str(x) + str(y), "goal_position": str(x - 2) + str(y + 2)}] + [
                                             {"current_position": str(x - 1) + str(y + 1),
                                              "goal_position": "*remove"}]])

        return self.chain_moves

    def crown_can_capture(self, x, y, direction):
        i = 1
        if direction == "top left":
            while True:
                if self.is_position(x - i, y - i) and self.is_position(x - i - 1, y - i - 1):
                    if self.board[x - i][y - i] == 'o' and self.board[x - i - 1][y - i - 1] == '-':
                        return [True, x - i - 1, y - i - 1]
                    i += 1
                else:
                    break
        elif direction == "top right":
            while True:
                if self.is_position(x - i, y + i) and self.is_position(x - i - 1, y + i + 1):
                    if self.board[x - i][y + i] == 'o' and self.board[x - i - 1][y + i + 1] == '-':
                        return [True, x - i - 1, y + i + 1]
                    i += 1
                else:
                    break
        return [False]

    def crown_captures(self, x, y, moves=None):
        if moves is None:
            moves = [0, []]
        left_capture = self.crown_can_capture(x, y, "top left")
        right_capture = self.crown_can_capture(x, y, "top right")

        # baas - ei saa süüa midagi
        if not left_capture[0] and not right_capture[0]:
            if moves[0] > self.longest_chain:
                self.longest_chain = moves[0]
                self.chain_moves = moves[1]
            return self.chain_moves

        # kui saab liikuda mõlemale poole
        if left_capture[0] and right_capture[0]:

            x_left = left_capture[1]
            y_left = left_capture[2]

            x_right = right_capture[1]
            y_right = right_capture[2]

            # vaatab kui palju saaks vasakule minnes võtta
            # märgib, millisel positsioonil liigutatav nupp ja kuhu selle liigutama peab (kui minna selle käiguga)
            self.crown_captures(x_left, y_left, [moves[0] + 1, moves[1] + [
                {"current_position": str(x) + str(y), "goal_position": str(x_left) + str(y_left)}] + [
                                                     {"current_position": str(x_left + 1) + str(y_left + 1),
                                                      "goal_position": "*remove"}]])
            # kui palju saaks paremale minnes võtta
            self.crown_captures(x_right, y_right, [moves[0] + 1, moves[1] + [
                {"current_position": str(x) + str(y), "goal_position": str(x_right) + str(y_right)}] + [
                                                       {"current_position": str(x_right + 1) + str(y_right - 1),
                                                        "goal_position": "*remove"}]])

        # vaatleme ainult vasakule võtmist
        elif left_capture[0]:
            x_left = left_capture[1]
            y_left = left_capture[2]

            self.crown_captures(x_left, y_left, [moves[0] + 1, moves[1] + [
                {"current_position": str(x) + str(y), "goal_position": str(x_left) + str(y_left)}] + [
                                                     {"current_position": str(x_left + 1) + str(y_left + 1),
                                                      "goal_position": "*remove"}]])

        # ainult paremale võtmist
        elif right_capture[0]:
            x_right = right_capture[1]
            y_right = right_capture[2]

            self.crown_captures(x_right, y_right, [moves[0] + 1, moves[1] + [
                {"current_position": str(x) + str(y), "goal_position": str(x_right) + str(y_right)}] + [
                                                       {"current_position": str(x_right + 1) + str(y_right - 1),
                                                        "goal_position": "*remove"}]])

        safety = 0

        if left_capture[0]:
            if not self.is_safe(left_capture[1], left_capture[2], left_capture[1] + 1, left_capture[2] + 1):
                safety = 3
        elif right_capture[0]:
            if not self.is_safe(right_capture[1], right_capture[2], right_capture[1] + 1, right_capture[2] - 1):
                safety = 3

        return [self.chain_moves, safety]

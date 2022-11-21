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

  def bestMoves(self):
    for x in range(self.size):
      for y in range(self.size):

        # boardil märgitud roboti nupud "10" ja vastase nupud "20"
        if self.board[x][y] == 10:
          self.getPriority(x, y)
    file_num = 1
    if not os.path.isdir("./moves"):
        try:
            os.mkdir("./moves")
        except OSError:
            print ("Directory creation failed")

    while (os.path.isfile("./moves/"+str(file_num)+".json")):
        file_num += 1
    print(file_num)
    for x in range(len(self.best_moves)):
        with open('./moves/'+str(file_num+x)+".json", 'w') as outfile:
            json.dump(self.best_moves[x], outfile)
    return self.best_moves

  def getPriority(self,x,y):
    capture_priority = 1
    top_left_priority = 1
    top_right_priority = 1

    # hiljem valime priority score järgi:
        # capture chain = 10*n
        # crowning = 29 (kui kunagi otsustame seda teha)
        # keeping a line = 1 * n
        # safe moves

    # leiame pikim käikude järjestuse
    captures = self.captures(x,y)
    if len(captures) > 0:
      capture_priority *= len(captures) * 10

    # leiame pikima nuppudest koosneva diagonaali
    if(self.isPosition(x-1, y-1) and self.board[x-1][y-1] == 0):
      top_left_priority += self.longest_line(x-1, y-1)
    if(self.isPosition(x-1, y+1) and self.board[x-1][y+1] == 0):
      top_right_priority += self.longest_line(x-1, y+1)

     # kuhu poole on safe liikuda, ei sööda ära
    if(self.isPosition(x-1, y-1) and self.board[x-1][y-1] == 0 and self.isSafe(x-1, y-1, x, y)):
      top_left_priority += 3
    if(self.isPosition(x-1, y+1) and self.board[x-1][y+1] == 0 and self.isSafe(x-1, y+1, x, y)):
      top_right_priority += 3

    # give priority to middle of board moves
    if(self.isPosition(x-1, y-1) and self.board[x-1][y-1] == 0 and y > 2 and y < 5):
      top_left_priority += 1
    if(self.isPosition(x-1, y+1) and self.board[x-1][y+1] == 0 and y > 2 and y < 5):
      top_right_priority += 1

    # valime mis siis parim edasine tegevus
    bestMove = max(capture_priority, top_left_priority, top_right_priority)

    # kui söömiste punktid paremad kui ükski priority score
    if(bestMove == capture_priority and bestMove > self.best_priority_score):
      # siis captured on kõige parem järgmine käik
      self.best_moves = captures
      self.best_priority_score = capture_priority

    # kui mõistlik liikuda vasakule
    elif(bestMove == top_left_priority and bestMove > self.best_priority_score):
      self.best_moves = [{"current_position": str(x)+str(y),"goal_position": str(x-1)+str(y-1)}]
      if(x==1): self.best_moves.append({"current_position": str(x-1)+str(y-1),"goal_position": "*crown"})
      self.best_priority_score = top_left_priority
    
    # kui mõistlik liikuda paremale
    elif(bestMove == top_right_priority and bestMove > self.best_priority_score):
      self.best_moves = [{"current_position": str(x)+str(y),"goal_position": str(x-1)+str(y+1)}]
      if(x==1): self.best_moves.append({"current_position": str(x-1)+str(y+1),"goal_position": "*crown"})
      self.best_priority_score = top_right_priority

    return self.best_moves

  # kui käia kohale (x,y), kas see on safe move
  def isSafe(self,x,y,prev_x,prev_y):
    # kõik muu intuitiivne, ei tea kas ma väsinud lihtsalt, aga ei saa aru miks see or seal tingimustes
    if(self.isPosition(x-1, y-1) and self.board[x-1][y-1] == 20 and self.isPosition(x+1, y+1)and (self.board[x+1][y+1] == 0 or (x+1 == prev_x and y+1 == prev_y))):
      return False

    if(self.isPosition(x-1, y+1) and self.board[x-1][y+1] == 20 and self.isPosition(x+1, y-1)and (self.board[x+1][y-1] == 0 or (x+1 == prev_x and y-1 == prev_y))):
      return False
    return True

  # pikim roboti nuppude rida (diagonaal)
  def longestLine(self,x,y):
    longest_left_to_right = 0
    longest_right_to_left = 0
    pos_x = x
    pos_y = y

    # top left to bottom right jagatud kaheks

    # center to top left
    while (self.isPosition(pos_x-1, pos_y-1) and self.board[pos_x-1][pos_y-1] == 10):
      longest_left_to_right+=1
      pos_x -= 1
      pos_y -= 1
    pos_x = x
    pos_y = y

    # center to bottom right
    while (self.isPosition(pos_x+1, pos_y+1) and self.board[pos_x+1][pos_y+1] == 10):
      longest_left_to_right+=1
      pos_x += 1
      pos_y += 1
    pos_x = x
    pos_y = y

    # top right to bottom left jagatud kaheks

    # center to top right 
    while (self.isPosition(pos_x-1, pos_y+1) and self.board[pos_x-1][pos_y+1] == 10):
      longest_right_to_left+=1
      pos_x -= 1
      pos_y += 1
    pos_x = x
    pos_y = y
            
    # center to bottom left
    while (self.isPosition(pos_x+1, pos_y-1) and self.board[pos_x+1][pos_y-1] == 10):
        longest_right_to_left+=1
        pos_x += 1
        pos_y -= 1

    return (max(longest_left_to_right, longest_right_to_left))

  # kas antud positsioon eksisteerib laual?
  def isPosition(self,x,y):
    if x >= 0 and x < self.size and y >= 0 and y < self.size:
      return True
    return False

  # kas saab etteantud suunas nuppu võtta?
  def canCapture(self,x,y,direction):
    if (direction == "top left"):
      if(self.isPosition(x-1,y-1) and self.isPosition(x-2,y-2) and self.board[x-1][y-1] == 20 and self.board[x-2][y-2] == 0):
        return True
    elif (direction == "top right"):
      if (self.isPosition(x-1,y+1) and self.isPosition(x-2, y+2) and self.board[x-1][y+1] == 20 and self.board[x-2][y+2] == 0):
        return True
    return False


  # kuhu liikudes saab süüa vastase nuppe (ja kui mitu järjest)
  def captures(self,x,y,moves = [0, []]):

    # baas - ei saa süüa midagi
    if not self.canCapture(x, y, "top left") and not self.canCapture(x, y, "top right"):
      if (moves[0] > self.longest_chain):
        self.longest_chain = moves[0]
        self.chain_moves = moves[1]
      return self.chain_moves

    # kui saab liikuda mõlemale poole
    if self.canCapture(x, y, "top left") and self.canCapture(x, y, "top right"):

      # vaatab kui palju saaks vasakule minnes võtta
      # märgib, millisel positsioonil liigutatav nupp ja kuhu selle liigutama peab (kui minna selle käiguga)
      self.captures(x-2, y-2, [ moves[0]+1, moves[1] + [{"current_position": str(x) +str(y) , "goal_position": str(x-2) + str(y-2)}] + [{"current_position": str(x-1) +str(y-1) , "goal_position": "*remove"}] ])
      # kui palju saaks paremale minnes võtta
      self.captures(x-2, y+2, [ moves[0]+1, moves[1] + [{"current_position": str(x) +str(y) , "goal_position": str(x-2) + str(y+2)}] + [{"current_position": str(x-1) +str(y+1) , "goal_position": "*remove"}] ])
    
    # vaatleme ainult vasakule võtmist
    elif self.canCapture(x, y, "top left"):
      self.captures(x-2, y-2, [ moves[0]+1, moves[1] + [{"current_position": str(x) +str(y) , "goal_position": str(x-2) + str(y-2)}] + [{"current_position": str(x-1) +str(y-1) , "goal_position": "*remove"}] ])

    # ainult paremale võtmist
    elif self.canCapture(x, y, "top right"):
      self.captures(x-2, y+2, [ moves[0]+1, moves[1] + [{"current_position": str(x) +str(y) , "goal_position": str(x-2) + str(y+2)}] + [{"current_position": str(x-1) +str(y+1) , "goal_position": "*remove"}] ])

    return self.chain_moves
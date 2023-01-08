import numpy as np

BOARD_SIZE = 480
SQUARE_SIZE = 60

camera_index = 0
arduino_com = "COM7"

# roboti nuppude värvid
ROBOT_LOW_VALUES = np.load("BoardDetection/variables/robotlowerlimits.npy")
ROBOT_HIGH_VALUES = np.load("BoardDetection/variables/robotupperlimits.npy")

# inimese nuppude värvid
OPPONENT_LOW_VALUES = np.load("BoardDetection/variables/opponentlowerlimits.npy")
OPPONENT_HIGH_VALUES = np.load("BoardDetection/variables/opponentupperlimits.npy")

ROBOT_CROWN_LOW_VALUES = np.load("BoardDetection/variables/robotcrownlowerlimits.npy")
ROBOT_CROWN_HIGH_VALUES = np.load("BoardDetection/variables/robotcrownupperlimits.npy")

OPPONENT_CROWN_LOW_VALUES = np.load("BoardDetection/variables/opponentcrownlowerlimits.npy")
OPPONENT_CROWN_HIGH_VALUES = np.load("BoardDetection/variables/opponentcrownupperlimits.npy")
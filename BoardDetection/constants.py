import numpy as np

BOARD_SIZE = 480
SQUARE_SIZE = 60

# roboti nuppude värvid
ROBOT_LOW_VALUES = np.load("BoardDetection/robotlowerlimits.npy")
ROBOT_HIGH_VALUES = np.load("BoardDetection/robotupperlimits.npy")

# inimese nuppude värvid
OPPONENT_LOW_VALUES = np.load("BoardDetection/opponentlowerlimits.npy")
OPPONENT_HIGH_VALUES = np.load("BoardDetection/opponentupperlimits.npy")

ROBOT_CROWN_LOW_VALUES = np.load("BoardDetection/robotcrownlowerlimits.npy")
ROBOT_CROWN_HIGH_VALUES = np.load("BoardDetection/robotcrownupperlimits.npy")

OPPONENT_CROWN_LOW_VALUES = np.load("BoardDetection/opponentcrownlowerlimits.npy")
OPPONENT_CROWN_HIGH_VALUES = np.load("BoardDetection/opponentcrownupperlimits.npy")
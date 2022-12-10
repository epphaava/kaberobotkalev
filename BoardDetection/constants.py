import numpy as np

BOARD_SIZE = 480
SQUARE_SIZE = 60

BLUE_LOW_VALUES = np.load("BoardDetection/bluelowerlimits.npy")
BLUE_HIGH_VALUES = np.load("BoardDetection/blueupperlimits.npy")

RED_LOW_VALUES = np.load("BoardDetection/redlowerlimits.npy")
RED_HIGH_VALUES = np.load("BoardDetection/redupperlimits.npy")

BLUE_CROWN_LOW_VALUES = np.array([37, 28, 142])
BLUE_CROWN_HIGH_VALUES = np.array([96, 85, 188])

RED_CROWN_LOW_VALUES = np.array([37, 28, 142])
RED_CROWN_HIGH_VALUES = np.array([96, 85, 188])
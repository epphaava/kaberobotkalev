import cv2
import gameplay.config as config
import gameplay.image_processing as image_processing
import gameplay.checkers as checkers


def text_board():
    # save the board as an image
    print('image written!')

    # get the state of the board as a matrix
    config.current_state = image_processing.board_array()

    current_board = checkers.Checkers(config.current_state)
    current_board.bestMoves()


def main():
    text_board()


if __name__ == "__main__":
    main()

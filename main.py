import cv2
import config
import image_processing
import checkers

camera = cv2.VideoCapture(0)

while True:
  ret, frame  = camera.read()

  if not ret:
    break


  if cv2.waitKey(1) & 0xFF == ord("q"):
    break

  elif cv2.waitKey(1)%256 == 32:
    # SPACE pressed
    
    # save the board as an image
    cv2.imwrite('test_img.jpg', frame)
    print('image written!')

    # get the state of the board as a matrix
    config.current_state = image_processing.board_array(config.current_state)

    current_board = checkers.Checkers(config.current_state)
    current_board.bestMoves()




# When everything done, release the camera
print("closing program")
camera.release()
cv2.destroyAllWindows()
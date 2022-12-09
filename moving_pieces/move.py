import corners_dict

# use this method to move the piece through corners to the given destination in best_moves

corners = {}

def move(best_moves):
    global corners

    if len(corners) == 0:
        corners = corners_dict.to_dict()




if __name__ == "__main__":
    move([])

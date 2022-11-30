# tagastab board state maatriksina
def board_array():
    f = open("../BoardDetection//abi.txt", "r")
    x = f.read().strip()
    state = []
    row = []
    k = 0
    for i in x:
        row.append(i)
        if k == 7:
            k = 0
            state.append(row)
            row = []
        else:
            k += 1
    print(state)
    return state

def main():
    board_array()

if __name__ == "__main__":
    main()
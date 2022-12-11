# SEDA VIST POLE VAJA, EI TEA MIS MA TEGELT MÕTLESIN SIIN

def to_dict():
    f = open("corners.txt", "r")
    corners = f.read().split("\n")
    matrix = []
    row = []
    for i in range(7):
        for j in range(7):
            row.append(corners[i * 7 + j])
        matrix.append(row)
        row = []
    dict = {}
    for row in range(7):
        for column in range(7):
            position = str(column) + str(row)
            sqr_crns = []
            if row != 0 and column != 6:
                sqr_crns.append(matrix[row - 1][6 - column - 1])
            if row != 0 and column != 0:
                sqr_crns.append(matrix[row - 1][6 - column])
            if row != 6 and column != 6:
                sqr_crns.append(matrix[row][6 - column - 1])
            if row != 6 and column != 0:
                sqr_crns.append(matrix[row][6 - column])
            dict.update({position : sqr_crns})
    print(dict)
    return dict

if __name__ == "__main__":
    to_dict()

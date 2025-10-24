import numpy as np
import json
from utils import rotate90, find_partner, check_distance, cal_distance, find_positions

# file_path = "./Problem/problem.json"
# key_feature = ["problem", "field", "entities"]
board = np.array([[5,5,7,2],
                  [0,3,6,0],
                  [4,7,2,4],
                  [1,6,3,1]])


def solver(board):
    """
    Using 2x2 only to rotate
    """
    shape = board.shape[0]
    total_pairs = (shape*shape)//2
    paired = np.full((shape,shape), False, dtype=bool)
    score = 0
    ops = []
    while score < total_pairs:
        for i in range(shape):
            for j in range(shape):
                if paired[i][j] == True:
                    continue
                
                ii, jj = find_partner(i, j, board, paired)
                
                # if check_distance(i,j,ii,jj):
                #     if abs(ii - i) == 1 and abs(jj-j) == 0:
                #         board = rotate90(j, i, 2, board)
                #         ops.append({"x": j, "y": i, "n": 2})
                #     ii, jj = find_positions(i, j, board) 
                #     paired[i][j] = True
                #     paired[ii][jj] = True
                #     score += 1
                #     continue
                
                dist = cal_distance(i,j,ii,jj)
                print(len(ops))
                print(board)
                while dist > 1:
                    if jj > j:
                        if j >= shape-2 and i >= shape-2:
                            if abs(ii-i) == 1 and abs(jj-i) == 1:
                                board = rotate90(j,i-1,2,board)
                                ops.append({"x": j, "y": i-1, "n": 2})
                                board = rotate90(j-2,i-1,3,board)
                                ops.append({"x": j-2, "y": i-1, "n": 3})
                                board = rotate90(j,i-1,2,board)
                                ops.append({"x": j, "y": i-1, "n": 2})
                                board = rotate90(j-2,i,2,board)
                                ops.append({"x": j-2, "y": i, "n": 2})
                                board = rotate90(j,i,2,board)
                                ops.append({"x": j, "y": i, "n": 2})
                                break

                        if (abs(ii-i) == 1 and abs(jj - j) > 1) or (abs(ii-i) > 1 and abs(jj-j) == 1) or (abs(ii-i) > 1 and abs(ii-i) > 1):
                            board = rotate90(jj-1, ii-1, 2, board)
                            ops.append({"x": jj-1, "y": ii-1, "n": 2})
                        elif (abs(ii-i) == 0 and abs(jj-j) > 1) or (abs(ii-i) == 1 and abs(jj-j) == 1 and jj == shape-1):
                            board = rotate90(jj-1, ii, 2, board)
                            ops.append({"x": jj-1, "y": ii, "n": 2})
                        elif abs(ii - i) == 1 and abs(jj - j) == 1 and jj < shape-1:
                            board = rotate90(jj, ii-1, 2, board)
                            ops.append({"x": jj, "y": ii-1, "n": 2}) 
                    else:
                        if abs(ii-i) > 1:
                            board = rotate90(jj, ii-1, 2, board)
                            ops.append({"x": jj, "y": ii-1, "n": 2})
                        elif abs(ii-i) == 1 and abs(jj-j) >= 1:
                            board = rotate90(jj, ii, 2, board)
                            ops.append({"x": jj, "y": ii, "n": 2})
                        elif abs(ii-i) == 1 and abs(jj-j) == 0:
                            break
                    print(i,j)  
                    ii,jj = find_positions(i,j,board)
                    dist = cal_distance(i,j,ii,jj)

                if check_distance(i,j,ii,jj):
                    if i < shape - 2:
                        if abs(ii - i) == 1 and abs(jj-j) == 0:
                            board = rotate90(j, i, 2, board)
                            ops.append({"x": j, "y": i, "n": 2}) 
                        ii, jj = find_positions(i, j, board)
                        paired[i][j] = True
                        paired[ii][jj] = True
                        score += 1
                    else:
                        if abs(ii - i) == 0 and abs(jj-j) == 1:
                            count = 0
                            while count <= 2:
                                board = rotate90(j,i,2,board)
                                ops.append({"x": j, "y": i, "n": 2}) 
                                count += 1  
                        ii, jj = find_positions(i, j, board)
                        paired[i][j] = True
                        paired[ii][jj] = True
                        score += 1
                
    return board, ops

if __name__ == "__main__":
    # board = np.array([[5,5,7,2],
    #               [0,3,6,0],
    #               [4,7,2,4],
    #               [1,6,3,1]])
    # board = np.array([[7,2,0,7],
    #                 [3,4,0,1],
    #                 [6,6,1,5],
    #                 [3,2,5,4]])

    #Special case
    # board = np.array([[47,16,39,48,51,69,8,59,2,70,30,52],
    #                    [17,65,46,45,12,46,29,43,36,40,65,47],
    #                    [54,1,4,26,54,27,32,57,41,23,29,13],
    #                    [52,14,31,9,16,18,22,22,12,15,39,61],
    #                    [60,51,71,17,30,44,7,37,69,55,48,55],
    #                    [11,4,61,31,41,25,28,70,64,8,58,9],
    #                    [20,59,10,53,68,38,44,28,19,37,71,67],
    #                    [24,13,68,33,32,42,3,20,49,27,40,34],
    #                    [60,58,21,26,5,63,34,35,43,14,56,49],
    #                    [24,33,6,56,50,1,66,0,2,10,23,57],
    #                    [21,36,18,63,19,66,45,6,7,0,5,11],
    #                    [3,62,50,15,53,62,25,64,35,67,42,38]])

    board = np.array([[0,1,1,2,3,4,4,5,5,6,6,7,8,8,9,10],[0,11,11,2,3,12,13,13,14,15,16,7,17,17,9,10],[18,18,19,20,21,12,22,22,14,15,16,23,23,24,24,25],[26,26,19,20,21,27,28,28,29,29,30,30,31,31,32,25],[33,33,34,35,35,27,36,37,37,38,38,39,40,41,32,42],[43,43,34,44,44,45,36,46,55,47,48,39,40,41,49,42],[50,51,51,52,53,45,54,46,55,47,48,56,57,57,49,58],[50,59,60,52,68,53,54,62,62,63,72,63,64,64,65,58],[66,59,60,67,61,61,69,70,71,71,73,56,74,74,65,75],[66,76,77,67,68,78,69,70,79,80,72,73,81,81,82,75],[83,76,77,84,85,78,86,86,79,80,87,87,88,88,82,89],[83,90,91,84,85,92,92,93,94,95,95,96,96,97,97,89],[98,90,91,99,100,101,101,93,94,102,103,104,105,106,106,107],[98,108,109,99,100,110,110,111,112,102,103,104,105,113,114,107],[115,108,109,116,116,117,117,111,112,118,118,119,119,113,114,120],[115,121,121,122,122,123,123,124,124,125,125,126,126,127,127,120]])

    new_board, ops = solver(board)
    print(f"Number of step: {len(ops)}")
    with open("answer.json", "w") as f:
        json.dump(ops, f)
    print(new_board)
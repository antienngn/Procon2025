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
                print(f"Current index {i,j}")
                print(f"Duplicate value {ii, jj}")
                if check_distance(i,j,ii,jj):
                    if abs(ii - i) == 1 and abs(jj-j) == 0:
                        board = rotate90(j, i, 2, board)
                        ops.append({"x": j, "y": i, "n": 2})

                    paired[i][j] = True
                    paired[i][j+1] = True
                    score += 1
                    continue

                dist = cal_distance(i,j,ii,jj)
                # print(board)
                # print(score,"\n")
                while dist > 1:
                    if jj > j:
                        if ii > i and jj - j > 1:
                            board = rotate90(jj-1, ii-1, 2, board)
                            ops.append({"x": jj-1, "y": ii-1, "n": 2})
                            # ii, jj = find_positions(i,j,board)
                        elif ii > i and jj - j == 1:
                            board = rotate90(jj, ii-1, 2, board)
                            ops.append({"x": jj, "y": ii-1, "n": 2}) 
                        elif ii == i:
                            board = rotate90(jj-1, ii, 2, board)
                            ops.append({"x": jj-1, "y": ii, "n": 2})
                            # ii, jj = find_positions(i,j,board)
                    else:
                        if abs(ii-i) > 1:
                            board = rotate90(jj, ii-1, 2, board)
                            ops.append({"x": jj, "y": ii-1, "n": 2})
                        elif abs(ii-i) == 1 and abs(jj-j) >= 1:
                            board = rotate90(jj, ii, 2, board)
                            ops.append({"x": jj, "y": ii, "n": 2})
                        elif abs(ii-i) == 1 and abs(jj-j) == 0:
                            break
                            # board = rotate90(j,i,2,board)
                            # ops.append({"x": j, "y": 2, "n": 2})
                    # print(board)
                    ii, jj = find_positions(i,j,board)
                    dist = cal_distance(i,j,ii,jj)
                if check_distance(i,j,ii,jj):
                    if abs(ii - i) == 1 and abs(jj-j) == 0:
                        board = rotate90(j, i, 2, board)
                        ops.append({"x": j, "y": i, "n": 2}) 
                    paired[i][j] = True
                    paired[i][j+1] = True
                    score += 1
                
    return board, ops

if __name__ == "__main__":
    board = np.array([[5,5,7,2],
                  [0,3,6,0],
                  [4,7,2,4],
                  [1,6,3,1]])
    new_board, ops = solver(board)
    print(f"Number of step: {len(ops)}")
    with open("answer.json", "w") as f:
        json.dump(ops, f)
    print(new_board)
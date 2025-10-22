import numpy as np
import json
from utils import rotate90, find_partner, check_distance, cal_distance, find_positions

file_path = "./Problem/problem.json"
key_feature = ["problem", "field", "entities"]

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
                if check_distance(i,j,ii,jj):
                    paired[i][j] = True
                    paired[ii][jj] = True
                    score += 1
                    continue

                dist = cal_distance(i,j,ii,jj)
                while dist > 1:
                    if abs(jj - j) > abs(ii - i):
                        board = rotate90(jj-1, ii-1, 2, board)
                        ops.append({"x": jj-1, "y": ii-1, "n": 2})
                    if abs(jj - j) < abs(ii - i):
                        board = rotate90(jj-1, ii, 2, board)
                        ops.append({"x": jj-1, "y": ii, "n": 2})
                    if jj > 0:
                        board = rotate90(jj, ii-1, 2, board)
                        ops.append({"x": jj, "y": ii-1, "n": 2})
                    ii, jj = find_positions(i,j,board)
                    if check_distance(i,j,ii,jj):
                        paired[i][j] = True
                        paired[ii][jj] = True
                        score += 1
                        break
                    update_dist = cal_distance(i,j,ii,jj)
                    if update_dist < dist:
                        dist = update_dist
    
    return board, ops

if __name__ == "__main__":
    board = np.array([[5,5,7,2],
                  [0,3,6,0],
                  [4,7,2,4],
                  [1,6,3,1]])
    new_board, ops = solver(board)
    print(f"Number of step: {len(ops)}")
    print(new_board)
import numpy as np
import json
import os
from utils import rotate90, find_partner, select_block 
from collections import defaultdict

file_path = "./Problem/problem.json"
key_feature = ["problem", "field", "entities"]

# board= np.array([[47,16,39,48,51,69,8,59,2,70,30,52],
#          [17,65,46,45,12,46,29,43,36,40,65,47],
#          [54,1,4,26,54,27,32,57,41,23,29,13],
#          [52,14,31,9,16,18,22,22,12,15,39,61],
#          [60,51,71,17,30,44,7,37,69,55,48,55],
#          [11,4,61,31,41,25,28,70,64,8,58,9],
#          [20,59,10,53,68,38,44,28,19,37,71,67],
#          [24,13,68,33,32,42,3,20,49,27,40,34],
#          [60,58,21,26,5,63,34,35,43,14,56,49],
#          [24,33,6,56,50,1,66,0,2,10,23,57],
#          [21,36,18,63,19,66,45,6,7,0,5,11],
#          [3,62,50,15,53,62,25,64,35,67,42,38]])

board = np.array([[5,5,7,2],
                  [0,3,6,0],
                  [4,7,2,4],
                  [1,6,3,1]])

def solver(board):
    shape = board.shape[0]
    total_pairs = (shape*shape)//2
    paired = np.full((shape,shape), False, dtype=bool)
    score = 0
    ops = []
    while score < total_pairs:
        for i in range(shape):
            for j in range(shape):
                if paired[i][j]:
                    continue
                    
                partner = find_partner(i,j, board, paired)
                if partner is None:
                    paired[i][j] = True
                    continue

                x,y = partner
                if abs(i-x) + abs(j-y) == 1:
                    paired[i][j] = True
                    paired[x][y] = True
                    score += 1
                    break

                while abs(i-x) + abs(j-y) != 1:
                    block = select_block(i,j,x,y,shape)
                    if block is None:
                        break
                    r,c,k = block
                    board = rotate90(i,j,k, board)
                    ops.append((j,i,k))
                    
                if abs(i - x) + abs(j - y) == 1:
                    print("H")
                    paired[i, j] = True
                    paired[x, y] = True
                    score += 1 
    return board, ops




if __name__ == "__main__":
    new_board, ops = solver(board=board)
    print(f"Number of step: {len(ops)}")
    print(new_board)
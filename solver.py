import numpy as np
import json
import os
from utils import extract_entities, rotate90
from collections import defaultdict

file_path = "./Problem/problem.json"
key_feature = ["problem", "field", "entities"]

def sum_pair_manhattan(board, n):
    pos = pair_positions(board)
    s = 0
    for v, lst in pos.items():
        if len(lst) != 2:
            continue
        (r1,c1),(r2,c2) = rc(n,lst[0]), rc(n,lst[1])
        s += abs(r1 - r2) + abs(c1 - c2)
    return s

def pair_positions(board):
    pos = defaultdict(list)
    for i,v in enumerate(board):
        pos[v].append(i)
    return pos

def solver():
    garden = extract_entities(file_path=file_path, key_feature=key_feature)
    rows, columns = garden.shape
    for i in rows:
        for j in columns:
            if garden[i][j] != garden[i+1][j+1]:
                rotate90(x_cord=0, y_cord=0, size=3, garden=garden)
    
    # print(temp)
    # return temp

def bfs():
    return        

if __name__ == "__main__":
    # print(np.array(extract_entities(file_path=file_path,key_feature=key_feature)))
    # print(solver())
    solver()
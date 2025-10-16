import json 
import numpy as np
from collections import defaultdict


def extract_entities(file_path, key_feature):
    try:
        with open(file_path, "r", encoding='utf-8') as f:
            data= json.load(f)
        current = data
        for key in key_feature:
            if key in current and isinstance(current, dict):
                current = current[key]
        problem = current
    except FileNotFoundError:
        print(f"File not found '{file_path}'.")

    return np.array(problem)

def rotate90(x_cord, y_cord, size, garden):
    sub = garden[y_cord:y_cord+size, x_cord:x_cord+size]
    garden[y_cord:y_cord+size, x_cord:x_cord+size] = np.flip(sub.T, axis=1)
    return garden

def find_partner(x,y, board, paired):
    v = board[x][y]
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if (i,j) != (x,y) and not paired[x][y] and board[i][j] == v:
                return (i,j)
    
    return None

def select_block(i1,j1,i2,j2,shape):
    for k in range(2,shape+1):
        row_min = max(0, min(i1,i2)-k+1)
        row_max = min(max(i1,i2), shape-k)
        col_min = max(0, min(j1,j2)-k+1)
        col_max = min(max(j1,j2), shape-k)

        for r in range(row_min, row_max+1):
            for c in range(col_min, col_max+1):
                if (r <= i1 < r + k and r <= i2 < r + k) and (c <= j1 < c + k and c <= j2 < c + k):
                    return (r,c,k)
    
    return None
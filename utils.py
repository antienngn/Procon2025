import json 
import numpy as np


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

def check_distance(x1,y1,x2,y2):
    if abs(x1-x2) + abs(y1-y2) == 1:
        return True
    return False

def cal_distance(x1,y1,x2,y2):
    return abs(x1-x2) + abs(y1-y2)

def find_positions(i_dup,j_dup,board):
    v = board[i_dup][j_dup]
    shape = board.shape[0]
    for i in range(shape):
        for j in range(shape):
            if (i,j) != (i_dup,j_dup) and board[i][j] == v:
                return (i,j)
    return None

def find_partner(x,y, board, paired):
    v = board[x][y]
    for i in range(board.shape[0]):
        for j in range(board.shape[0]):
            if (i,j) != (x,y) and not paired[i][j] and board[i][j] == v:
                return (i,j)
    return None, None
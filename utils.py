import json 
import numpy as np
import math


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

def rotate90(x_cord, y_cord, size, n_iterations, garden, ops, r=0):
    for i in range(n_iterations):
        sub = garden[y_cord:y_cord+size, x_cord:x_cord+size]
        try:
            garden[y_cord:y_cord+size, x_cord:x_cord+size] = np.flip(sub.T, axis=1)
        except:
            print("Error: cannot rotate", "\n", garden, garden[y_cord][x_cord], x_cord, y_cord)
            exit(0)
        ops.append({"x": x_cord, "y": y_cord+r, "n": size})
    return garden

def check_distance(x1,y1,x2,y2):
    if abs(x1-x2) + abs(y1-y2) == 1:
        return True
    return False

def cal_distance(x1,y1,x2,y2):
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return (dx+dy)

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

    
def select_dynamic_block_last_two_rows(x1,y1,x2,y2):
    x_cord,y_cord,size, n_iterations = 1,1,1,1
    dx = abs(x1-x2)
    dy = abs(y1-y2)
    if y1 < y2:
        if dx == 1 and dy == 1:
            x_cord,y_cord,size,n_iterations = (x2-1,y2-1,2,1)
        else:
            x_cord,y_cord,size,n_iterations = (x2,y2-1,2,2)
    else:
        x_cord,y_cord,size,n_iterations = (x2,y2,2,1)

    return x_cord,y_cord,size,n_iterations    

def select_dynamic_block(x1,y1,x2,y2,board):
    x_cord,y_cord,size, n_iterations = 1,1,1,1
    shape = board.shape[0]
    dx = abs(x1-x2)
    dy = abs(y1-y2)
    if x1 < x2:
        if dy == 0:
            if dx < abs(y2-shape):
                x_cord,y_cord,size,n_iterations = (x1,y1,dx+1,3)
            else:
                x_cord,y_cord,size,n_iterations = (x2-abs(y2-shape)+1,y1,abs(y2-shape),1)
        elif dy == 1 and y2 < y1:
            if abs(x2-x1+1) <= abs(y2-shape):
                x_cord,y_cord,size,n_iterations = (x1+1,y2,dx,3)
            else:
                x_cord,y_cord,size,n_iterations = (x2-abs(y2-shape)+1,y2,abs(y2-shape),3)
        else:
            xx = x1+1
            yy = y1-1
            if abs(xx-x2) == abs(yy-y2):
                x_cord,y_cord,size,n_iterations = (x1+1,y1-1,abs(yy-y2)+1,2)
            else:
                if dx == dy:
                    x_cord, y_cord, size, n_iterations = (x1,y1,dy+1,2)
                if dx > dy:
                    x_cord,y_cord,size,n_iterations = (x2-dy,y2-dy,dy+1,1)
                if dx < dy:
                    x_cord, y_cord, size, n_iterations = (x2-dx,y2-dx,dx+1,1)
    else:
        if dy == 0:
            if dx < abs(y2-shape):
                x_cord,y_cord,size,n_iterations = (x2,y2,dx+1,1)
            else:
                x_cord,y_cord,size,n_iterations = (x2,y2,abs(y2-shape),1)
        elif dx == 0:
            if dy < abs(x1-shape):
                x_cord,y_cord,size,n_iterations = (x1, y1, dy+1,1)
            else:
                x_cord,y_cord,size,n_iterations = (x1,y2-abs(x1-shape)+1,abs(x1-shape),1)
            
        elif dy == 1 and dx != 1:
            x_cord,y_cord,size,n_iterations = (x2,y2-1,2, 1)
        else:
            if dx == dy:
                x_cord, y_cord, size, n_iterations = (x2,y1,dy+1,2)
            else:
                if dy < abs(x2-shape):
                    x_cord,y_cord,size,n_iterations = (x2,y2-dy,dy+1, 1)
                else:
                    x_cord,y_cord,size,n_iterations = (x2,y2-abs(x2-shape)+1, abs(x2-shape),1)
    
    return (x_cord,y_cord,size, n_iterations)
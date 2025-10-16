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
        for j in range(board.shape[0]):
            if (i,j) != (x,y) and not paired[i][j] and board[i][j] == v:
                return (i,j)
    return None

def select_block(i, j, x, y, shape):
    dx, dy = x - i, y - j
    abs_dx, abs_dy = abs(dx), abs(dy)

    # 1) Chọn cạnh cho A
    if abs_dx >= abs_dy:
        side = 'right' if dx > 0 else 'left'
    else:
        side = 'top'   if dy > 0 else 'bottom'

    # 2) Chọn k = bước di chuyển + 1, trong [2..n]
    k = max(abs_dx, abs_dy) + 1
    k = min(max(k, 2), shape)

    # 3) Tính r,c để A nằm đúng trên cạnh side
    if side == 'top':
        r = i
        c = j - (k // 2)
    elif side == 'bottom':
        r = i - (k - 1)
        c = j - (k // 2)
    elif side == 'left':
        c = j
        r = i - (k // 2)
    else:  # 'right'
        c = j - (k - 1)
        r = i - (k // 2)

    # 4) Clamp vào biên [0..n-k]
    r = max(0, min(r, shape - k))
    c = max(0, min(c, shape - k))

    # 5) Đảm bảo A nằm trong block; B không nằm trong block
    if not (r <= i < r + k and c <= j < c + k):
        return None
    if (r <= x < r + k and c <= y < c + k):
        return None
    
    return (r, c, k)
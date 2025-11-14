import numpy as np
import json
from utils import rotate90,cal_distance,check_distance,find_partner

def count_pairs(board):
    try:
        if hasattr(board, "tolist"):
            board = board.tolist()
    except Exception:
        pass

    n = len(board)
    if n == 0:
        return 0
    m = len(board[0])

    pairs = 0
    for i in range(n):
        for j in range(m):
            if j + 1 < m and board[i][j] == board[i][j+1]:
                pairs += 1
            if i + 1 < n and board[i][j] == board[i+1][j]:
                pairs += 1
    return pairs

def paired_mask(board, paired, shape):
    for i in range(shape):
        for j in range(shape):
            if j + 1 < shape and board[i, j] == board[i, j + 1]:
                paired[i, j] = paired[i, j + 1] = True
            if i + 1 < shape and board[i, j] == board[i + 1, j]:
                paired[i, j] = paired[i + 1, j] = True
    
    return paired

def is_corner_region(x,y,size,n):
    return (x == 0 or x + size == n) and (y == 0 or y + size == n)

def subboard_is_paired(boards):
    mask_paired = []
    for board in boards:
        shape_x = board.shape[0]
        shape_y = board.shape[1]
        if shape_x != shape_y:
            mask_paired.append(False)
        
        paired = np.full((shape_x,shape_x), False, dtype=bool)
        region_paired = paired_mask(board,paired,shape_x)
        false_mask = np.logical_not(region_paired)
        num_unpaired = np.sum(false_mask)
        if num_unpaired == 1:
            return mask_paired.append(True)
    return mask_paired


def possible_subboard_rotate(x1, y1, x2, y2, board):
    """
    Return x_cord, y_cord, size board for simulation
    """
    sub_boards = []
    sub_boards_mask = None
    shape = board.shape[0]
    dx = abs(x1-x2)
    dy = abs(y1-y2)
    # if dx != 0 and dy != 0:
    #     x1 = x1+1
    #     y1 = y1-1
    #     dx = abs(x1-x2)
    #     dy = abs(y1-y2)
    if dx == 0:
        if dy > x1:
            sub_boards.append(board[y1:y2+1, x1:x1+dy+1])
        if dy > abs(x1-shape):
            sub_boards.append(board[y1:y2+1, x1-(dy+1):x1+1])
        else: 
            sub_boards.append(board[y1:y2+1, x1:x1+dy+1], board[y1:y2+1, x1-(dy+1):x1+1])
        
    elif dy == 0:
        if dx > abs(y2-shape):
            sub_boards.append(board[y2-dx:y2+1,x2-dx:x2+1])
        elif dx > y2:
            sub_boards.append(board[y1:y1+dx+1, x1:x1+dx+1])
        else:
            sub_boards.append(board[y2-dx:y2+1,x2-dx:x2+1], board[y1:y1+dx+1, x1:x1+dx+1])
        
    return sub_boards


def rotate_simulator(rotable_cells,board):
    """
    Return x_cord,y_cord,size,n_iter for rotate update
    """
    n = board.shape[0]
    current_pairs = count_pairs(board)
    ops = []


def solver_special(board, ops, paired):
    shape = board.shape[0]
    paired_checked = paired_mask(board,paired,shape)
    for i in range(shape):
        for j in range(shape):
            if paired_checked[i][j] == True:
                continue
            ii, jj = find_partner(i , j, board, paired)
            rotate_cells = possible_subboard_rotate(j,i,jj,ii,board)
            rotate_ops = rotate_simulator(rotate_cells, board)
            for op in rotate_ops:
                x_cord, y_cord, size, n_iter = op
                board = rotate90(x_cord,y_cord,size,n_iter,board,ops,r=0)
            paired_checked = paired_mask(board,paired,shape)
    return board,ops


if __name__ == "__main__":
    board = np.array()

    shape = board.shape[0]
    ops = []
    paired = np.full((shape,shape), False, dtype=bool)

    board,ops = solver_special(board,ops,paired)
    print(f"Number of step: {len(ops)}")
    with open("answer_special.json", "w") as f:
        json.dump(ops, f)
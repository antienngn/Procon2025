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
    Return list of x_cord, y_cord, size board for simulation
    Have two target point (under, on the right)
    """
    rotable_cells = []
    dx = abs(x1-x2)
    dy = abs(y1-y2)
    if dx == dy:
    
    else:
    
    return rotable_cells




def rotate90_simulator(x_cord, y_cord, size, n_iterations, garden):
    for i in range(n_iterations):
        sub = garden[y_cord:y_cord+size, x_cord:x_cord+size]
        try:
            garden[y_cord:y_cord+size, x_cord:x_cord+size] = np.flip(sub.T, axis=1)
        except:
            print("Error: cannot rotate", "\n", garden, garden[y_cord][x_cord], x_cord, y_cord)
            exit(0)
    return garden

def find_max_number_of_pairs(arr, key):
    if not arr or not arr[0]:
        return None  

    max_element = arr[0][0]
    max_value = max_element.get(key)

    for row in arr:
        for dictionary in row:
            current_value = dictionary.get(key)
            if current_value is not None and (max_value is None or current_value > max_value):
                max_value = current_value
                max_element = dictionary
    return max_element


def rotate_simulator(rotable_cells,board):
    """
    Return x_cord,y_cord,size,n_iter (dictionary format) for rotate update
    """
    best_ops = dict()
    ancestor_board = board.copy()
    ancestor_board_pairs = count_pairs(ancestor_board)
    simulator_pairs = []
    for i,cell in enumerate(rotable_cells):
        simulator_pairs[i] = []
        for n in range(1,4):
            simulator_board = rotate90_simulator(cell["x_cord"],cell["y_cord"],cell["size"],n,ancestor_board)
            simulator_pairs[i].append({"x_cord": cell["x_cord"],
                                       "y_cord": cell["y_cord"],
                                       "size": cell["size"],
                                       "n_iter": n,
                                        "number_of_pair":count_pairs(simulator_board)})
    
    highest_num_pair = find_max_number_of_pairs(simulator_pairs, "number_of_pair")
    if ancestor_board_pairs < highest_num_pair["number_of_pair"]:
        best_ops["x_cord"] = highest_num_pair["x_cord"]
        best_ops["y_cord"] = highest_num_pair["y_cord"]
        best_ops["size"] = highest_num_pair["size"]
        best_ops["n_iter"] = highest_num_pair["n_iter"]

    return best_ops


def solver_special(board, ops, paired):
    shape = board.shape[0]
    paired_checked = paired_mask(board,paired,shape)
    for i in range(shape):
        for j in range(shape):
            if paired_checked[i][j] == True:
                continue

            ii, jj = find_partner(i , j, board, paired)
            rotate_cells = possible_subboard_rotate(j,i,jj,ii,board)

            rotate_op = rotate_simulator(rotate_cells, board)
            x_cord = rotate_op["x_cord"]
            y_cord = rotate_op["y_cord"]
            size = rotate_op["size"]
            n_iter = rotate_op["n_iter"]

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
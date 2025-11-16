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


# def possible_subboard_rotate(x1, y1, x2, y2, board):
#     """
#     Return list of x_cord, y_cord, size board for simulation
#     Have two target point (under, on the right)
#     """
#     rotable_cells = []
#     H,W = board.shape
#     dx = abs(x1-x2)
#     dy = abs(y1-y2)
#     dx_board = [(x2,y2,dx),(x2-dx,y2,dx),(x2,y2-dx,dx),(x2-dx,y2-dy,dx)]
#     dy_board = [(x2,y2,dy),(x2-dy,y2,dy),(x2,y2-dy,dy),(x2-dy,y2-dy,dy)]
#     for i range (H,W):

        


#     return rotable_cells

def possible_subboard_rotate(x1, y1, x2, y2, board, paired_global=None):
    """
    Return a list of subboards that:
    (1) contain both (x1,y1) and (x2,y2)
    (2) have (x2,y2) at one of the 4 corners of the square
    (3) do NOT break existing global pairs inside this subboard
    """
    H, W = board.shape
    rotable_cells = []

    # Compute min square size that can include both points
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    min_size = max(dx, dy) + 1

    # If global paired mask is not provided, compute it
    if paired_global is None:
        paired_global = np.full((H, H), False, dtype=bool)
        for i in range(H):
            for j in range(W):
                if j+1 < W and board[i, j] == board[i, j+1]:
                    paired_global[i, j] = paired_global[i, j+1] = True
                if i+1 < H and board[i, j] == board[i+1, j]:
                    paired_global[i, j] = paired_global[i+1, j] = True

    # Try all possible sizes from min_size → full board
    for size in range(min_size, min(H, W) + 1):

        # Subboard must contain BOTH points, compute possible TL ranges
        min_tx = max(0, min(x1, x2) - (size - 1))
        max_tx = min(min(x1, x2), W - size)
        min_ty = max(0, min(y1, y2) - (size - 1))
        max_ty = min(min(y1, y2), H - size)

        if min_tx > max_tx or min_ty > max_ty:
            continue

        for tx in range(min_tx, max_tx + 1):
            for ty in range(min_ty, max_ty + 1):

                # -------------- (A) CHECK CORNER CONDITION ----------------
                corners = [
                    (tx, ty),
                    (tx + size - 1, ty),
                    (tx, ty + size - 1),
                    (tx + size - 1, ty + size - 1)
                ]
                if (x2, y2) not in corners:
                    continue

                # -------------- (B) CHECK THAT PAIRED CELLS REMAIN PAIRED --------------
                sub = board[ty:ty+size, tx:tx+size]
                local_paired = np.full((size, size), False, dtype=bool)

                # compute local pairs for the subboard
                for i in range(size):
                    for j in range(size):
                        if j+1 < size and sub[i, j] == sub[i, j+1]:
                            local_paired[i, j] = local_paired[i, j+1] = True
                        if i+1 < size and sub[i, j] == sub[i+1, j]:
                            local_paired[i, j] = local_paired[i+1, j] = True

                # Now check consistency with global paired mask
                # If a cell is paired globally AND lies inside this subboard
                # then it must be paired in local_paired
                consistent = True
                for i in range(size):
                    for j in range(size):
                        global_i = ty + i
                        global_j = tx + j
                        if paired_global[global_i, global_j] and not local_paired[i, j]:
                            consistent = False
                            break
                    if not consistent:
                        break

                if not consistent:
                    continue

                # Passed all conditions
                rotable_cells.append({
                    "x_cord": tx,
                    "y_cord": ty,
                    "size": size
                })

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
    simulator_pairs = [[] for _ in range(len(rotable_cells))]
    for i,cell in enumerate(rotable_cells):
        for n in range(1,4):
            temp = ancestor_board.copy()
            simulator_board = rotate90_simulator(cell["x_cord"],cell["y_cord"],cell["size"],n,temp)
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
            rotate_cells = possible_subboard_rotate(j,i,jj,ii,board,paired)

            rotate_op = rotate_simulator(rotate_cells, board)
            x_cord = rotate_op["x_cord"]
            y_cord = rotate_op["y_cord"]
            size = rotate_op["size"]
            n_iter = rotate_op["n_iter"]

            board = rotate90(x_cord,y_cord,size,n_iter,board,ops,r=0)

            paired_checked = paired_mask(board,paired,shape)
    return board,ops


if __name__ == "__main__":
    board = np.array([[0,0,1,2,2,3,4,5,6,6,7,8],[9,9,1,10,11,3,4,5,12,12,7,8],[13,14,14,10,11,15,15,16,16,17,18,18],[13,19,20,20,21,22,22,29,29,23,24,24],[25,19,26,27,21,28,28,30,30,23,31,32],[25,33,26,27,34,35,36,37,31,17,37,32],[38,33,39,40,34,35,36,41,42,42,43,44],[38,45,39,40,46,47,47,41,48,49,43,44],[50,45,51,52,46,53,53,54,48,49,55,55],[50,56,51,52,57,57,58,54,59,60,61,61],[62,56,63,63,64,64,58,65,59,60,66,67],[62,68,68,69,69,70,70,65,71,71,66,67]])

    shape = board.shape[0]
    ops = []
    paired = np.full((shape,shape), False, dtype=bool)

    board,ops = solver_special(board,ops,paired)
    print(f"Number of step: {len(ops)}")
    with open("answer_special.json", "w") as f:
        json.dump(ops, f)
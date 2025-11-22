import numpy as np
import json
from collections import deque
from utils import rotate90,find_partner,count_pairs
from solver_general import solver 

def paired_mask(board, paired, shape):
    for i in range(shape):
        for j in range(shape):
            if j + 1 < shape and board[i, j] == board[i, j + 1]:
                paired[i, j] = paired[i, j + 1] = True
            if i + 1 < shape and board[i, j] == board[i + 1, j]:
                paired[i, j] = paired[i + 1, j] = True
    
    return paired

def subboard_is_paired(board, paired_global, tx, ty, size):
    """
    Kiểm tra subboard (tx, ty, size) có làm MẤT cặp nào đã ghép trong paired_global hay không.

    board: board tổng
    paired_global: mask đôi trong board tổng (True nếu ô đang thuộc cặp)
    tx, ty: top-left
    size: kích thước subboard
    """
    sub = board[ty:ty+size, tx:tx+size]
    local_paired = np.full((size, size), False, dtype=bool)

    for i in range(size):
        for j in range(size):
            if j + 1 < size and sub[i, j] == sub[i, j+1]:
                local_paired[i, j] = local_paired[i, j+1] = True
            if i + 1 < size and sub[i, j] == sub[i+1, j]:
                local_paired[i, j] = local_paired[i+1, j] = True

    for i in range(size):
        for j in range(size):
            gi = ty + i
            gj = tx + j
            if paired_global[gi, gj]:
                if not local_paired[i, j]:
                    return False, local_paired
                
    return True, local_paired

def subboard_is_paired_general(board, paired_global, tx, ty, size):
    """
    Kiểm tra subboard có phá cặp global không.
    Nếu phá mà ở viền subboard có thể xoay 1 cụm 2x2 (minirotate) thì sửa trực tiếp vào board.
    """
    paired_or_not = False
    paired_or_not, local_paired = subboard_is_paired(board,paired_global,tx,ty,size)
    if paired_or_not == False:
        shape = board.shape[0]
        for j in range(size-1):
            if ty - 1 < 0:
                break
            if (not local_paired[0][j]) and (not local_paired[0][j+1]) and (board[ty][tx+j] == board[ty-1][tx+j]) and (board[ty][tx+j+1] == board[ty-1][tx+j+1]):
                bx = tx + j
                by = ty
                board = rotate90(bx, by-1, 2, 1, board, ops, r=0)
                # print(board[by-1][bx])
                paired_global = paired_mask(board, paired_global, shape)

        #===========================
        # 2) BOTTOM EDGE  (i = size-1)
        #===========================
        for j in range(size-1):
            if ty + size > shape - 1:
                break
            if (not local_paired[size-1][j]) and (not local_paired[size-1][j+1]) and (board[ty+size-1][tx+j] == board[ty+size][tx+j]) and (board[ty+size-1][tx+j+1] == board[ty+size][tx+j+1]):
                # block nằm trên bottom
                bx = tx + j
                by = ty + size - 1
                # print(board[by][bx])
                board = rotate90(bx, by, 2, 1, board, ops, r=0)
                paired_global = paired_mask(board, paired_global, shape)

        #===========================
        # 3) LEFT EDGE  (j = 0)
        #===========================
        for i in range(size-1):
            # print(f"When value is")
            if tx - 1 < 0:
                break
            if (not local_paired[i][0]) and (not local_paired[i+1][0]) and (board[ty+i][tx] == board[ty+i][tx-1]) and (board[ty+i+1][tx] == board[ty+i+1][tx-1]):
                bx = tx
                by = ty + i
                # print(board[by][bx-1])
                board = rotate90(bx-1, by, 2, 1, board, ops, r=0)
                paired_global = paired_mask(board, paired_global, shape)

        #===========================
        # 4) RIGHT EDGE (j = size-1)
        #===========================
        for i in range(size-1):
            if tx + size > shape - 1:
                break
            if (not local_paired[i][size-1] == False) and (not local_paired[i+1][size-1] == False) and (board[ty+i][tx+size-1] == board[ty+i][tx+size]) and (board[ty+i+1][tx+size-1] == board[ty+i+1][tx+size]):
                bx = tx + size - 1
                by = ty + i
                board = rotate90(bx, by, 2, 1, board, ops, r=0)
                paired_global = paired_mask(board, paired_global, shape)

    paired_or_not,local_paired = subboard_is_paired(board,paired_global,tx,ty,size)
    return paired_or_not




def possible_subboard_rotate(x1, y1, x2, y2, board, paired):
    """
    Return list of x_cord, y_cord, size board for simulation
    Have two target point (under, on the right)
    """
    shape = board.shape[0]
    rotable_cells = []
    dx = abs(x1-x2)
    dy = abs(y1-y2)
    if dx == 0:
        size = dy  
        dy_board = [
            (x1,y1,size),
            (x2,       y2,       size),
            (x2-(size-1),  y2,       size),
            (x2,       y2-(size-1),  size),
            (x2-(size-1),  y2-(size-1),  size)
        ]
        candidates = dy_board

    # ==========================
    # CASE 2: dy = 0 
    # ==========================
    elif dy == 0:
        size = dx  
        dx_board = [
            (x1,y1,size),
            (x2,y2,size),
            (x2-(size-1),y2,size),
            (x2,y2-(size-1),size),
            (x2-(size-1),y2-(size-1),size)
        ]
        candidates = dx_board

    # ==========================
    # CASE 3: dx>0 & dy>0 
    # ==========================
    else:
        dx_board = [
            (x1,y1-dx,dx+1),
            (x1,y1,dx+1),
            (x2,y2,dx+1),
            (x2-dx,y2,dx+1),
            (x2,y2-dx,dx+1),
            (x2-dx,y2-dx,dx+1)
        ]
        dy_board = [
            (x1,y1-dy,dy+1),
            (x1,y1,dy+1),
            (x2,y2,dy+1),
            (x2-dy,y2,dy+1),
            (x2,y2-dy,dy+1),
            (x2-dy,y2-dy,dy+1)
        ]
        candidates = dx_board + dy_board
    # print(f"Before pruning: {candidates}")
    for (tx_raw, ty_raw, base_size) in candidates:
        tx = tx_raw
        ty = ty_raw
        size = base_size
        if tx < 0 or ty < 0:
            continue
        if size < 2:
            continue
        if tx + size > shape or ty + size > shape:
            continue
        if not subboard_is_paired(board, paired, tx, ty, size):
            continue

        rotable_cells.append({
            "x_cord": tx,
            "y_cord": ty,
            "size": size
        })
    # print(f"After pruning {rotable_cells}")
    return rotable_cells

def possible_subboard_general(x1, y1, x2, y2, board, paired,ops):
    """
    Return list of x_cord, y_cord, size board for simulation
    Have two target point (under, on the right)
    """
    shape = board.shape[0]
    rotable_cells = []
    dx = abs(x1-x2)
    dy = abs(y1-y2)
    if dx == 0:
        size = dy  
        dy_board = [
            (x1,y1,size),
            (x2,       y2,       size),
            (x2-(size-1),  y2,       size),
            (x2,       y2-(size-1),  size),
            (x2-(size-1),  y2-(size-1),  size)
        ]
        candidates = dy_board

    # ==========================
    # CASE 2: dy = 0 
    # ==========================
    elif dy == 0:
        size = dx  
        dx_board = [
            (x1,y1,size),
            (x2,y2,size),
            (x2-(size-1),y2,size),
            (x2,y2-(size-1),size),
            (x2-(size-1),y2-(size-1),size)
        ]
        candidates = dx_board

    # ==========================
    # CASE 3: dx>0 & dy>0 
    # ==========================
    else:
        dx_board = [
            (x1,y1-dx,dx+1),
            (x1,y1,dx+1),
            (x2,y2,dx+1),
            (x2-dx,y2,dx+1),
            (x2,y2-dx,dx+1),
            (x2-dx,y2-dx,dx+1)
        ]
        dy_board = [
            (x1,y1-dy,dy+1),
            (x1,y1,dy+1),
            (x2,y2,dy+1),
            (x2-dy,y2,dy+1),
            (x2,y2-dy,dy+1),
            (x2-dy,y2-dy,dy+1)
        ]
        candidates = dx_board + dy_board
    # print(f"Before pruning: {candidates}")
    for (tx_raw, ty_raw, base_size) in candidates:
        tx = tx_raw
        ty = ty_raw
        size = base_size
        if tx < 0 or ty < 0:
            continue
        if size < 2:
            continue
        if tx + size > shape or ty + size > shape:
            continue
        if not subboard_is_paired_general(board, paired, tx, ty, size):
            continue

        rotable_cells.append({
            "x_cord": tx,
            "y_cord": ty,
            "size": size
        })
    # print(f"After pruning {rotable_cells}")
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

def find_max_number_of_pairs(arr, key, step_key):
    if not arr or not arr[0]:
        return None

    best = None
    best_value = -float("inf")
    best_step = float("inf")

    for row in arr:
        for dic in row:
            if dic is None:
                continue

            value = dic.get(key)
            step = dic.get(step_key)

            if value is None or step is None:
                continue

            if value > best_value:
                best = dic
                best_value = value
                best_step = step

            elif value == best_value and step < best_step:
                best = dic
                best_step = step

    return best


def rotate_simulator(rotable_cells,board):
    """
    Return x_cord,y_cord,size,n_iter (dictionary format) for rotate update
    """
    best_ops = dict()
    shape = board.shape[0]
    total_paired = (shape*shape)//2
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
    highest_num_pair = find_max_number_of_pairs(simulator_pairs, "number_of_pair", "n_iter")
    if not highest_num_pair:
        return 
    if ancestor_board_pairs < highest_num_pair["number_of_pair"]:
        best_ops["x_cord"] = highest_num_pair["x_cord"]
        best_ops["y_cord"] = highest_num_pair["y_cord"]
        best_ops["size"] = highest_num_pair["size"]
        best_ops["n_iter"] = highest_num_pair["n_iter"] 
    return best_ops


def solver_special(board, ops, paired):
    shape = board.shape[0]
    paired_checked = paired_mask(board,paired,shape)
    total_pairs = (shape*shape)//2
    skip_values = set()
    while True:
        cant_rotate_more = False
        for i in range(shape):
            for j in range(shape):
                if paired_checked[i][j] == True:
                    continue

                cell_value = board[i][j]
                if cell_value in skip_values:
                    continue

                # print(f"{i,j,board[i][j]}")
                ii, jj = find_partner(i , j, board, paired_checked)
                if ii is None or jj is None:
                    skip_values.add(board[i][j])   
                    continue

                rotate_cells = possible_subboard_rotate(j,i,jj,ii,board,paired_checked)
                if not rotate_cells:
                    skip_values.add(cell_value)
                    continue

                rotate_op = rotate_simulator(rotate_cells, board)
                if not rotate_op:
                    skip_values.add(cell_value)
                    continue

                x_cord = rotate_op["x_cord"]
                y_cord = rotate_op["y_cord"]
                size = rotate_op["size"]
                n_iter = rotate_op["n_iter"]
                board = rotate90(x_cord,y_cord,size,n_iter,board,ops,r=0)
                paired_checked = paired_mask(board,paired,shape)

                cant_rotate_more = True
                
        if count_pairs(board) == total_pairs:
            return board,ops,True

        if not cant_rotate_more:
            break
    
    for val in list(skip_values):
        for i in range(shape):
            for j in range(shape):
                if paired_checked[i][j] == True:
                    continue
                if board[i][j] == val:
                    ii, jj = find_partner(i,j, board, paired_checked)
                    if ii is None or jj is None: 
                        continue

                    rotate_rollback = possible_subboard_general(j, i , jj, ii, board, paired_checked,ops)
                    rotate_op = rotate_simulator(rotate_rollback, board)

                    if not rotate_op:
                        continue
                    x_cord = rotate_op["x_cord"]
                    y_cord = rotate_op["y_cord"]
                    size = rotate_op["size"]
                    n_iter = rotate_op["n_iter"]
                    board = rotate90(x_cord,y_cord,size,n_iter,board,ops,r=0)
                    paired_checked = paired_mask(board,paired,shape)

    if count_pairs(board) == total_pairs:
        return board,ops,True
    
    return board,ops,False


def get_unpaired_bounds(paired_checked):
    coords = [(i,j) for i in range(paired_checked.shape[0])
                     for j in range(paired_checked.shape[1])
                     if not paired_checked[i,j]]
    rows = [i for i,j in coords]
    cols = [j for i,j in coords]
    return min(rows), max(rows), min(cols), max(cols)

def find_safe_subboard(board, paired_checked,ops):
    """
    Tìm subboard nhỏ nhất (rectangle hoặc square) bao tất cả unpaired
    nhưng không phá các cặp đã ghép (dùng subboard_is_paired để kiểm tra).
    Mở rộng rectangle nếu cần để đạt trạng thái SAFE.
    """
    shape = board.shape[0]

    # Step 1 : bounding rectangle of all unpaired
    min_r, max_r, min_c, max_c = get_unpaired_bounds(paired_checked)
    rect_h = max_r - min_r + 1
    rect_w = max_c - min_c + 1

    # ============================================
    # 2. Square size tối thiểu bao bounding rectangle
    # ============================================
    S = max(rect_h, rect_w)
    if S < 2:
        S = 2

    # ============================================
    # 3. Thử square từ size S trở đi
    # ============================================
    while True:

        # thử mọi vị trí r0, c0 sao cho square trùm rectangle
        # r0 <= min_r <= max_r <= r0 + S - 1
        # c0 <= min_c <= max_c <= c0 + S - 1
        start_r = min_r - (S - rect_h)
        end_r   = min_r
        start_c = min_c - (S - rect_w)
        end_c   = min_c

        found_position = False

        for r0 in range(start_r, end_r + 1):
            for c0 in range(start_c, end_c + 1):
                r1 = r0 + S - 1
                c1 = c0 + S - 1

                # 3a. Square phải nằm trong board
                if r0 < 0 or c0 < 0 or r1 >= shape or c1 >= shape:
                    continue

                found_position = True

                # ---------------------------------------------------
                # 3b. Check SAFE bằng subboard_is_paired (square)
                # ---------------------------------------------------
                ok, _ = subboard_is_paired(board, paired_checked, c0, r0, S)
                if ok:
                    sub = board[r0:r1+1, c0:c1+1].copy()
                    return sub, (r0, r1, c0, c1)

                # ---------------------------------------------------
                # 3c. Nếu square không SAFE → thử sửa viền
                # ---------------------------------------------------
                temp_board = board.copy()
                temp_paired = paired_checked.copy()

                ok_fix = subboard_is_paired_general(temp_board,
                                                    temp_paired,
                                                    c0, r0, S)

                if ok_fix:
                    # Nếu sửa được → cập nhật board + trả subboard mới
                    board[:] = temp_board[:]
                    paired_checked[:] = paired_mask(board, paired_checked, shape)
                    sub = board[r0:r1+1, c0:c1+1].copy()
                    return sub, (r0, r1, c0, c1)

        # ---------------------------------------------------
        # 4. Nếu không có vị trí nào hợp lệ → tăng square size
        # ---------------------------------------------------
        if not found_position:
            raise RuntimeError("Không thể tạo square bao trọn unpaired!")

        S += 1
        if S > shape:
            raise RuntimeError("Square vượt kích thước board!")


def solver_hybrid(board, ops):
    shape = board.shape[0]
    paired = np.full((shape,shape), False, dtype=bool)
    board_after_special, ops, ok = solver_special(board, ops, paired)
    if ok:
        print("Solver_special: solved entire board!")
        return board_after_special, ops
    return board,[]
    # ---------------------------------------------------
    # 2) Tính paired_checked sau special
    # ---------------------------------------------------
    # paired_checked = paired_mask(board_after_special, paired, shape)

    # ---------------------------------------------------
    # 3) Tạo subboard an toàn nhỏ nhất
    # ---------------------------------------------------
    # subboard, (r0, r1, c0, c1) = find_safe_subboard(board_after_special, paired_checked,ops)

    # print(f"SAFE SUBBOARD bounds: rows {r0}..{r1},  cols {c0}..{c1},  shape={subboard.shape}")

    # # ---------------------------------------------------
    # # 4) Chạy solver_general trên subboard an toàn
    # # ---------------------------------------------------
    # solved_sub, sub_ops = solver(subboard)

    # # ---------------------------------------------------
    # # 5) Ghép subboard solved trở lại board lớn + offset ops
    # # ---------------------------------------------------
    # board_after_special[r0:r1+1, c0:c1+1] = solved_sub

    # for op in sub_ops:
    #     ops.append({
    #         "x": op["x"] + c0,
    #         "y": op["y"] + r0,
    #         "n": op["n"]
    #     })


    # return board_after_special, ops


# if __name__ == "__main__":
#     # board = np.array([[0,1,2,3,3,4,5,5,6,6,7,8,9,10,11,11,12,13,13,14],[0,1,2,15,16,4,17,18,19,20,7,8,9,10,21,22,12,23,24,14],[25,25,26,15,16,27,17,18,19,20,28,28,29,29,40,40,21,23,24,31],[32,32,26,33,34,27,35,36,37,37,38,38,39,39,41,41,22,42,43,31],[44,45,45,33,34,46,35,36,47,47,48,48,49,50,51,30,30,42,43,52],[44,53,54,55,55,46,56,56,57,58,58,59,49,50,60,61,51,62,63,52],[64,53,54,65,66,66,67,67,57,68,68,59,69,69,60,61,70,62,63,71],[64,72,73,65,74,75,75,76,77,77,78,79,80,81,82,82,70,83,84,71],[85,72,73,86,74,87,88,76,89,90,78,79,80,81,91,91,92,83,84,93],[85,94,95,86,96,87,88,97,89,90,98,99,99,100,100,101,92,102,103,93],[104,94,95,105,96,106,107,97,108,109,98,110,110,111,112,101,113,102,103,114],[104,115,116,105,117,106,107,118,108,109,119,119,120,111,112,121,113,122,123,114],[124,115,116,125,117,126,126,118,127,127,128,128,120,129,130,121,131,122,123,132],[124,133,134,125,135,136,176,166,155,147,136,139,140,129,130,141,131,142,143,132],[144,133,134,145,135,146,167,167,155,147,137,139,140,150,150,141,151,142,143,152],[144,153,153,145,154,146,177,156,156,148,137,158,159,159,160,160,151,161,162,152],[163,164,164,165,154,166,178,157,157,148,138,158,169,169,170,171,171,161,162,172],[163,173,173,165,174,175,168,168,149,149,138,179,180,181,189,170,182,183,183,172],[184,184,185,186,174,175,176,187,177,178,188,179,180,181,189,182,190,191,192,192],[193,193,185,186,194,194,199,187,195,195,188,196,196,197,197,199,190,191,198,198]])
#     # board = np.array([[0,0,1,2,2,3,4,5,6,6,7,8],[9,9,1,10,11,3,4,5,12,12,7,8],[13,14,14,10,11,15,15,16,16,17,18,18],[13,19,20,20,21,22,22,29,29,23,24,24],[25,19,26,27,21,28,28,30,30,23,31,32],[25,33,26,27,34,35,36,37,31,17,37,32],[38,33,39,40,34,35,36,41,42,42,43,44],[38,45,39,40,46,47,47,41,48,49,43,44],[50,45,51,52,46,53,53,54,48,49,55,55],[50,56,51,52,57,57,58,54,59,60,61,61],[62,56,63,63,64,64,58,65,59,60,66,67],[62,68,68,69,69,70,70,65,71,71,66,67]])
#     # board = np.array([[0,1,1,2,3,4,4,5,5,6,6,7,8,8,9,10],[0,11,11,2,3,12,13,13,14,15,16,7,17,17,9,10],[18,18,19,20,21,12,22,22,14,15,16,23,23,24,24,25],[26,26,19,20,21,27,28,28,29,29,30,30,31,31,32,25],[33,33,34,35,35,27,36,37,37,38,38,39,40,41,32,42],[43,43,34,44,44,45,36,46,55,47,48,39,40,41,49,42],[50,51,51,52,53,45,54,46,55,47,48,56,57,57,49,58],[50,59,60,52,68,53,54,62,62,63,72,63,64,64,65,58],[66,59,60,67,61,61,69,70,71,71,73,56,74,74,65,75],[66,76,77,67,68,78,69,70,79,80,72,73,81,81,82,75],[83,76,77,84,85,78,86,86,79,80,87,87,88,88,82,89],[83,90,91,84,85,92,92,93,94,95,95,96,96,97,97,89],[98,90,91,99,100,101,101,93,94,102,103,104,105,106,106,107],[98,108,109,99,100,110,110,111,112,102,103,104,105,113,114,107],[115,108,109,116,116,117,117,111,112,118,118,119,119,113,114,120],[115,121,121,122,122,123,123,124,124,125,125,126,126,127,127,120]])
#     # board = np.array([[0,1,2,2,3,4,5,5,6,7,7,8],[0,1,9,10,3,4,11,12,6,13,14,8],[15,15,9,10,16,17,11,12,18,13,14,19],[20,21,21,22,16,17,23,23,18,24,25,19],[20,26,27,22,28,29,30,31,31,24,25,32],[33,26,27,34,28,29,30,35,36,36,37,32],[33,38,44,38,39,39,40,35,41,41,37,42],[43,43,44,34,45,46,40,47,48,48,49,42],[50,51,52,53,45,46,54,47,55,55,49,56],[50,51,52,53,57,58,58,59,66,60,61,56],[62,62,63,64,57,65,54,59,67,60,61,68],[69,69,63,64,70,70,65,71,66,67,71,68]])
#     # board = np.array([[0,0,1,2,2,3,3,4,5,5,6,6],[7,46,33,33,20,20,8,8,12,13,14,15],[7,39,39,26,26,16,16,1,12,13,14,15],[19,40,40,27,27,21,9,9,23,24,24,25],[19,47,34,34,28,21,17,10,23,31,31,25],[32,48,35,35,28,22,17,10,36,36,37,38],[32,41,41,29,29,22,11,11,43,44,37,38],[45,52,42,30,30,18,18,4,42,44,49,50],[45,46,51,51,47,48,52,53,43,54,49,50],[55,56,57,58,59,60,60,61,53,54,62,62],[55,67,56,58,59,63,63,61,64,65,65,66],[67,68,57,68,69,69,70,70,64,71,71,66]])

#     # board = np.array([[51,42,42,56,56,8,8,44,44,7,7,58],[51,55,24,24,0,0,17,61,2,2,39,58],[40,55,66,41,41,6,17,61,37,65,39,30],[40,54,68,13,13,6,14,14,37,31,23,30],[28,54,67,21,21,63,63,16,47,66,23,22],[28,43,50,45,45,36,19,16,47,68,15,22],[53,43,27,25,25,36,19,64,69,67,15,10],[53,59,50,29,29,3,3,64,69,12,26,10],[38,59,27,70,60,48,9,9,46,34,26,35],[38,32,18,70,60,48,57,57,46,31,1,35],[20,32,71,49,12,18,71,65,34,49,1,62],[20,52,52,5,5,11,11,33,33,4,4,62]])
#     # board = np.array([[0,0,1,1,2,2,3,3,4,5,5,6],[7,7,8,9,10,11,12,12,4,13,14,6],[44,33,33,20,20,15,16,17,18,13,14,19],[44,37,25,25,21,15,16,17,18,24,24,19],[45,37,26,26,21,8,29,29,30,30,31,32],[38,38,27,27,22,9,34,35,35,36,31,32],[46,39,28,28,22,10,40,40,41,36,42,43],[47,39,34,23,23,11,47,48,41,49,42,43],[50,51,45,52,46,53,66,58,53,49,55,55],[50,51,56,52,57,58,59,59,48,60,61,61],[62,63,56,64,57,65,67,54,54,60,68,68],[62,63,70,64,70,65,66,71,67,69,69,71]])
#     # board = np.array([[71,31,2,2,121,121,33,33,117,119,99,99,41,41,1,89],[71,49,46,123,31,66,55,55,117,119,22,22,108,108,1,89],[123,49,21,59,39,127,127,97,56,56,3,118,118,32,45,45],[46,30,21,59,38,101,101,25,90,90,3,53,53,32,103,7],[5,30,51,61,78,78,58,107,26,107,58,73,88,91,103,7],[5,85,8,44,66,93,79,79,64,64,98,73,88,91,9,114],[95,95,8,44,51,93,126,126,124,124,98,110,110,111,9,114],[70,100,15,15,61,85,0,0,97,75,11,116,24,111,80,80],[70,100,77,77,92,26,25,43,94,75,11,116,24,47,12,12],[23,72,10,67,92,39,76,43,94,6,52,112,35,47,84,84],[23,72,10,67,54,18,62,125,125,6,52,112,35,62,86,104],[74,96,96,87,54,18,38,57,57,60,60,76,106,106,86,104],[74,68,102,87,4,120,120,17,109,16,19,19,27,27,29,115],[82,68,102,69,4,36,65,17,109,16,34,34,113,113,29,115],[82,122,122,69,63,36,65,28,37,14,50,81,42,20,40,40],[13,13,48,48,63,83,83,28,37,14,50,81,42,20,105,105]])
#     # board = np.array([[0,0,1,2,209,209,198,175,175,163,151,139,125,114,102,91,66,283,228,252,3,3,16,17],[18,18,1,2,224,199,199,176,176,163,151,139,115,115,102,91,67,283,227,252,4,4,24,17],[25,25,253,253,210,210,187,187,177,164,140,140,116,116,92,92,68,282,238,238,5,5,38,38],[39,40,239,239,225,211,188,188,177,164,141,141,117,117,93,93,69,282,237,237,6,6,53,53],[39,256,284,284,225,211,200,178,178,152,152,126,126,103,103,94,70,274,236,251,19,7,62,63],[64,247,276,265,78,34,34,258,229,216,215,214,228,227,226,226,71,281,236,250,19,7,221,63],[76,257,51,75,89,33,50,262,274,273,273,272,260,271,259,270,72,281,235,235,20,8,207,85],[86,258,59,59,101,33,49,121,132,144,156,170,181,193,203,217,73,272,224,249,20,8,185,100],[86,248,50,74,113,32,32,120,132,144,155,169,180,192,202,216,79,287,234,234,21,9,185,109],[110,259,49,74,113,22,48,120,131,131,155,169,180,192,202,215,79,271,223,248,22,9,160,109],[124,249,58,58,137,21,47,119,130,130,154,168,168,191,191,214,80,286,233,233,10,10,160,134],[135,260,48,257,241,240,55,66,67,68,69,70,71,72,73,213,81,270,232,232,11,11,149,147],[148,250,47,278,277,287,78,40,77,208,197,186,161,161,137,213,81,280,221,247,12,12,136,147],[148,251,57,278,277,276,90,64,89,29,29,30,30,31,31,212,275,206,231,231,23,13,111,172],[173,261,57,255,254,266,90,76,101,43,44,44,45,46,46,212,28,42,41,26,23,13,111,172],[173,261,45,255,254,242,114,87,112,275,263,104,118,118,119,104,28,27,27,26,14,14,88,195],[196,262,56,243,243,242,125,87,112,99,106,127,127,128,129,94,222,60,36,36,15,15,88,195],[196,263,56,230,218,229,138,110,136,99,105,142,143,128,129,207,222,61,37,37,24,16,77,219],[220,264,43,204,218,217,138,124,150,80,105,142,143,153,154,184,184,206,51,35,65,65,54,219],[220,264,55,204,194,203,162,135,150,98,98,165,166,153,167,208,223,52,52,35,42,41,54,245],[246,265,240,182,194,193,162,149,174,97,97,165,166,179,167,156,133,133,121,106,82,82,75,245],[246,266,241,182,171,181,186,159,174,96,96,189,189,179,190,145,145,122,122,107,83,83,60,267],[268,256,269,157,171,170,198,159,197,95,95,200,201,201,190,157,146,123,123,107,84,84,61,279],[268,286,269,280,285,279,267,244,244,230,205,205,183,183,158,158,146,134,108,108,100,85,62,285]])
#     # board = np.array([[16,4,47,28,22,67,56,52,54,48,2,70],[64,27,58,55,62,31,40,62,33,51,7,45],[1,59,10,71,64,18,21,0,19,15,60,5],[42,23,34,69,45,16,7,49,41,38,42,17],[15,59,13,26,25,43,44,36,53,23,60,32],[14,17,20,5,50,33,66,43,61,34,57,21],[54,70,47,66,39,20,13,30,8,48,12,52],[29,68,44,1,63,6,51,65,3,28,0,40],[67,18,56,69,71,38,26,46,9,41,68,39],[49,63,37,10,58,30,57,19,50,9,24,61],[29,12,65,55,11,32,31,3,11,2,6,8],[46,22,24,4,36,53,27,14,35,37,25,35]])
#     shape = board.shape[0]
#     total_pairs = (shape*shape)//2
#     ops = []
#     # paired = np.full((shape,shape), False, dtype=bool)

#     # board,ops = solver_special(board,ops,paired)
#     board,ops = solver_hybrid(board,ops)
#     print(f"Number of step: {len(ops)}")
#     if count_pairs(board) == total_pairs:
#         print("Success")
#     else:
#         print("Not optimal")
#     with open("answer_special.json", "w") as f:
#         json.dump(ops, f)
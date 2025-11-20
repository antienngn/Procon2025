import numpy as np
import json
from utils import rotate90,find_partner

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

def on_edge_subboard(board, paired_global, tx, ty, size):
    shape = board.shape[0]
    sub_mask = [[False for _ in range(size)] for _ in range(size)]
    false_cells = []

    # ----------------------------
    # Tạo sub_mask và thu thập FALSE
    # ----------------------------
    for i in range(size):
        for j in range(size):
            gi = ty + i
            gj = tx + j

            if 0 <= gi < shape and 0 <= gj < shape:
                if not paired[gi][gj]:
                    sub_mask[i][j] = True
                    false_cells.append((i, j))
            else:
                # Điểm nằm ngoài board = không phải FALSE real
                sub_mask[i][j] = False

    # Nếu không có FALSE → không dùng rule này
    if len(false_cells) == 0:
        return False, sub_mask

    # ----------------------------------------------------
    # STEP 1: TẤT CẢ FALSE phải nằm trên boundary subboard
    # ----------------------------------------------------
    def on_boundary(i, j):
        return (i == 0 or j == 0 or i == size - 1 or j == size - 1)

    for (i, j) in false_cells:
        if not on_boundary(i, j):
            return False, sub_mask  # FAIL do có false interior

    # ----------------------------------------------------
    # STEP 2: Kiểm tra có FALSE liền nhau trên boundary
    # ----------------------------------------------------

    # Duyệt viền theo clockwise order
    boundary = []

    # Top row
    for j in range(size):
        boundary.append((0, j))
    # Right column
    for i in range(1, size):
        boundary.append((i, size-1))
    # Bottom row (right → left)
    for j in range(size-2, -1, -1):
        boundary.append((size-1, j))
    # Left column (bottom → top)
    for i in range(size-2, 0, -1):
        boundary.append((i, 0))

    # Tạo list giá trị False/True theo biên
    border_vals = []
    for (i, j) in boundary:
        border_vals.append(sub_mask[i][j])

    # Check adjacent FALSE
    for idx in range(len(border_vals) - 1):
        if border_vals[idx] and border_vals[idx+1]:
            return True, sub_mask

    # wrap-around: điểm đầu và cuối
    if border_vals[0] and border_vals[-1]:
        return True, sub_mask

    # Không có cặp false cạnh nhau
    return False, sub_mask

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
            # nếu global nói ô này thuộc 1 cặp
            if paired_global[gi, gj]:
                if not local_paired[i, j]:
                    return False
                
    return True

def possible_subboard_rotate(x1, y1, x2, y2, board, paired, ops):
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
            (x2,y2,dx+1),
            (x2-dx,y2,dx+1),
            (x2,y2-dx,dx+1),
            (x2-dx,y2-dx,dx+1)
        ]
        dy_board = [
            (x2,y2,dy+1),
            (x2-dy,y2,dy+1),
            (x2,y2-dy,dy+1),
            (x2-dy,y2-dy,dy+1)
        ]
        candidates = dx_board + dy_board
    print(f"Before pruning: {candidates}")
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
        print(f"After pruning {rotable_cells}")
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
    ancestor_board = board.copy()
    ancestor_board_pairs = count_pairs(ancestor_board)
    simulator_pairs = [[] for _ in range(len(rotable_cells))]
    # print(f"Rotable cells is {rotable_cells}")
    print(board)
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
    total_paired = (shape*shape)//2
    current_paired = count_pairs(board)
    wait_list = []
    while current_paired < total_paired:
        for i in range(shape):
            for j in range(shape):
                if paired_checked[i][j] == True:
                    continue
                
                ii, jj = find_partner(i , j, board, paired_checked)
                print(f"Print {ii,jj, board[i][j]}")
                rotate_cells = possible_subboard_rotate(j,i,jj,ii,board,paired_checked, ops)
                if not rotate_cells or board[i][j] in wait_list:
                    if board[i][j] not in wait_list:
                        wait_list.append(board[i][j])
                    continue
                rotate_op = rotate_simulator(rotate_cells, board)
                if not rotate_op:
                    continue
                x_cord = rotate_op["x_cord"]
                y_cord = rotate_op["y_cord"]
                size = rotate_op["size"]
                n_iter = rotate_op["n_iter"]
                board = rotate90(x_cord,y_cord,size,n_iter,board,ops,r=0)
                paired_checked = paired_mask(board,paired,shape)
                if board[i][j] in wait_list:
                    wait_list.remove(board[i][j])
        count += 1
        print(f"N iter: {count}")
        temp = count_pairs(board)
        if temp == current_pairs:
            print(board)
            break
        current_pairs = temp
    return board,ops


if __name__ == "__main__":
    # board = np.array([[0,1,2,3,3,4,5,5,6,6,7,8,9,10,11,11,12,13,13,14],[0,1,2,15,16,4,17,18,19,20,7,8,9,10,21,22,12,23,24,14],[25,25,26,15,16,27,17,18,19,20,28,28,29,29,40,40,21,23,24,31],[32,32,26,33,34,27,35,36,37,37,38,38,39,39,41,41,22,42,43,31],[44,45,45,33,34,46,35,36,47,47,48,48,49,50,51,30,30,42,43,52],[44,53,54,55,55,46,56,56,57,58,58,59,49,50,60,61,51,62,63,52],[64,53,54,65,66,66,67,67,57,68,68,59,69,69,60,61,70,62,63,71],[64,72,73,65,74,75,75,76,77,77,78,79,80,81,82,82,70,83,84,71],[85,72,73,86,74,87,88,76,89,90,78,79,80,81,91,91,92,83,84,93],[85,94,95,86,96,87,88,97,89,90,98,99,99,100,100,101,92,102,103,93],[104,94,95,105,96,106,107,97,108,109,98,110,110,111,112,101,113,102,103,114],[104,115,116,105,117,106,107,118,108,109,119,119,120,111,112,121,113,122,123,114],[124,115,116,125,117,126,126,118,127,127,128,128,120,129,130,121,131,122,123,132],[124,133,134,125,135,136,176,166,155,147,136,139,140,129,130,141,131,142,143,132],[144,133,134,145,135,146,167,167,155,147,137,139,140,150,150,141,151,142,143,152],[144,153,153,145,154,146,177,156,156,148,137,158,159,159,160,160,151,161,162,152],[163,164,164,165,154,166,178,157,157,148,138,158,169,169,170,171,171,161,162,172],[163,173,173,165,174,175,168,168,149,149,138,179,180,181,189,170,182,183,183,172],[184,184,185,186,174,175,176,187,177,178,188,179,180,181,189,182,190,191,192,192],[193,193,185,186,194,194,199,187,195,195,188,196,196,197,197,199,190,191,198,198]])
    # board = np.array([[0,0,1,2,2,3,4,5,6,6,7,8],[9,9,1,10,11,3,4,5,12,12,7,8],[13,14,14,10,11,15,15,16,16,17,18,18],[13,19,20,20,21,22,22,29,29,23,24,24],[25,19,26,27,21,28,28,30,30,23,31,32],[25,33,26,27,34,35,36,37,31,17,37,32],[38,33,39,40,34,35,36,41,42,42,43,44],[38,45,39,40,46,47,47,41,48,49,43,44],[50,45,51,52,46,53,53,54,48,49,55,55],[50,56,51,52,57,57,58,54,59,60,61,61],[62,56,63,63,64,64,58,65,59,60,66,67],[62,68,68,69,69,70,70,65,71,71,66,67]])
    # board = np.array([[0,1,1,2,3,4,4,5,5,6,6,7,8,8,9,10],[0,11,11,2,3,12,13,13,14,15,16,7,17,17,9,10],[18,18,19,20,21,12,22,22,14,15,16,23,23,24,24,25],[26,26,19,20,21,27,28,28,29,29,30,30,31,31,32,25],[33,33,34,35,35,27,36,37,37,38,38,39,40,41,32,42],[43,43,34,44,44,45,36,46,55,47,48,39,40,41,49,42],[50,51,51,52,53,45,54,46,55,47,48,56,57,57,49,58],[50,59,60,52,68,53,54,62,62,63,72,63,64,64,65,58],[66,59,60,67,61,61,69,70,71,71,73,56,74,74,65,75],[66,76,77,67,68,78,69,70,79,80,72,73,81,81,82,75],[83,76,77,84,85,78,86,86,79,80,87,87,88,88,82,89],[83,90,91,84,85,92,92,93,94,95,95,96,96,97,97,89],[98,90,91,99,100,101,101,93,94,102,103,104,105,106,106,107],[98,108,109,99,100,110,110,111,112,102,103,104,105,113,114,107],[115,108,109,116,116,117,117,111,112,118,118,119,119,113,114,120],[115,121,121,122,122,123,123,124,124,125,125,126,126,127,127,120]])
    # board = np.array([[0,1,2,2,3,4,5,5,6,7,7,8],[0,1,9,10,3,4,11,12,6,13,14,8],[15,15,9,10,16,17,11,12,18,13,14,19],[20,21,21,22,16,17,23,23,18,24,25,19],[20,26,27,22,28,29,30,31,31,24,25,32],[33,26,27,34,28,29,30,35,36,36,37,32],[33,38,44,38,39,39,40,35,41,41,37,42],[43,43,44,34,45,46,40,47,48,48,49,42],[50,51,52,53,45,46,54,47,55,55,49,56],[50,51,52,53,57,58,58,59,66,60,61,56],[62,62,63,64,57,65,54,59,67,60,61,68],[69,69,63,64,70,70,65,71,66,67,71,68]])
    # board = np.array([[0,1,2,2,3,55,41,17,17,3,6,7,7,8,8,9,10,10,11,12,12,13,13,14],[31,0,15,15,16,42,42,18,18,4,6,22,22,23,24,9,25,26,11,27,28,29,30,14],[31,1,32,32,246,223,223,209,198,184,161,161,149,137,125,116,100,92,67,67,55,41,16,37],[38,39,40,40,246,224,224,199,199,184,162,162,149,137,125,116,101,79,79,68,152,152,43,37],[38,39,54,54,247,232,210,210,185,185,163,163,150,138,117,117,101,80,80,68,151,151,43,63],[64,64,65,66,247,232,211,211,186,186,164,164,150,138,126,102,102,81,81,69,21,20,19,63],[77,78,65,66,248,225,225,200,200,175,175,155,170,169,169,168,167,166,165,165,21,20,19,90],[77,78,91,92,248,226,226,201,201,187,176,155,144,143,142,154,154,153,153,140,5,5,4,90],[98,99,91,100,249,233,212,212,202,187,176,131,144,143,142,141,141,129,128,140,139,139,33,113],[98,99,114,115,249,233,213,213,202,177,177,131,121,120,130,130,119,129,128,127,127,126,33,113],[124,124,114,115,234,234,227,203,203,188,166,110,121,120,108,107,119,118,118,105,104,103,34,134],[135,135,136,136,235,235,227,204,204,188,167,110,109,109,108,107,106,106,93,105,104,103,23,134],[147,147,148,148,236,236,214,214,189,189,168,87,95,95,86,94,94,85,93,84,83,82,24,158],[159,159,280,268,253,244,221,221,197,197,183,174,160,73,86,72,71,85,70,84,83,82,35,158],[173,173,280,268,245,245,222,222,209,198,183,174,160,73,59,72,71,58,70,57,56,69,25,181],[182,182,281,269,254,252,252,251,251,239,238,250,250,49,59,48,47,58,46,57,56,44,26,181],[196,196,281,269,254,241,241,240,240,239,238,237,237,49,35,48,47,34,46,45,45,44,36,207],[208,208,282,270,255,231,230,230,229,229,216,228,228,145,122,122,96,96,75,75,51,51,27,207],[219,220,282,270,255,218,218,217,217,205,216,215,215,132,132,111,111,88,88,61,61,52,28,231],[219,220,287,256,256,195,194,206,206,205,192,191,190,133,133,112,112,89,89,62,62,52,29,242],[243,244,271,271,257,195,194,193,193,179,192,191,190,146,123,123,97,97,76,76,53,53,30,242],[243,253,272,272,257,172,180,180,171,179,170,178,178,259,260,261,262,262,263,264,264,265,265,266],[267,267,283,258,258,172,157,156,171,36,60,60,87,273,260,261,274,274,263,275,276,277,278,266],[279,279,283,273,259,146,157,156,145,50,50,74,74,284,284,285,285,286,286,275,276,277,278,287]])
    # board = np.array([[51,42,42,56,56,8,8,44,44,7,7,58],[51,55,24,24,0,0,17,61,2,2,39,58],[40,55,66,41,41,6,17,61,37,65,39,30],[40,54,68,13,13,6,14,14,37,31,23,30],[28,54,67,21,21,63,63,16,47,66,23,22],[28,43,50,45,45,36,19,16,47,68,15,22],[53,43,27,25,25,36,19,64,69,67,15,10],[53,59,50,29,29,3,3,64,69,12,26,10],[38,59,27,70,60,48,9,9,46,34,26,35],[38,32,18,70,60,48,57,57,46,31,1,35],[20,32,71,49,12,18,71,65,34,49,1,62],[20,52,52,5,5,11,11,33,33,4,4,62]])
    board = np.array([[56,60,60,59,58,58,52,51,57,56,0,7],[57,49,48,39,31,25,15,15,0,6,47,14],[62,49,54,2,3,3,4,4,5,19,53,14],[62,36,41,47,46,46,45,45,44,19,53,1],[63,36,41,40,40,34,33,32,39,29,52,8],[64,29,38,28,27,34,33,32,31,37,51,8],[59,18,30,28,27,26,26,20,25,37,44,9],[65,18,24,22,22,21,21,20,16,50,43,10],[66,5,13,11,10,9,17,17,16,50,1,11],[61,61,13,43,2,48,35,35,23,23,12,12],[67,54,7,6,67,55,55,42,42,38,30,24],[68,68,69,69,63,64,71,65,66,70,70,71]])
    shape = board.shape[0]
    ops = []
    paired = np.full((shape,shape), False, dtype=bool)

    board,ops = solver_special(board,ops,paired)
    print(f"Number of step: {len(ops)}")
    print("Successful!")
    with open("answer_special.json", "w") as f:
        json.dump(ops, f)
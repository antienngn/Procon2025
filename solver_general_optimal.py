import numpy as np
import json
from utils import rotate90, find_partner, cal_distance, find_positions


def select_dynamic_block_rows(x1, y1, x2, y2, board):
    shape = board.shape[0]
    dx, dy = abs(x1 - x2), abs(y1 - y2)

    x_cord = y_cord = size = n_iter = 1
    min_iter = float('inf')

    if x1 < x2:
        xx, yy = x1 + 1, y1 - 1
        dxx, dyy = abs(xx - x2), abs(yy - y2)

        # Check diagonal first
        if dxx == dyy and 2 < min_iter:
            min_iter = 2
            x_cord, y_cord, size, n_iter = x1 + 1, y1 - 1, dyy + 1, 2
        elif dxx == 0 and dyy < abs(x2 - shape) and 1 < min_iter:
            min_iter = 1
            x_cord, y_cord, size, n_iter = xx, yy, dyy + 1, 1
        elif dyy == 0 and dxx < abs(y2 - shape) and 3 < min_iter:
            min_iter = 3
            x_cord, y_cord, size, n_iter = xx, yy, dxx + 1, 3

        if min_iter != float('inf'):
            return x_cord, y_cord, size, n_iter

        # Horizontal
        if dy == 0:
            if dx < abs(y2 - shape):
                x_cord, y_cord, size, n_iter = x1, y1, dx + 1, 3
            else:
                x_cord, y_cord, size, n_iter = x2 - abs(y2 - shape) + 1, y1, abs(y2 - shape), 1

        # Slight diagonal
        elif dy == 1 and y2 < y1:
            if abs(x2 - x1 + 1) <= abs(y2 - shape):
                x_cord, y_cord, size, n_iter = x1 + 1, y2, dx, 3
            else:
                x_cord, y_cord, size, n_iter = x2 - abs(y2 - shape) + 1, y2, abs(y2 - shape), 3

        # General diagonal / other cases
        else:
            xx, yy = x1 + 1, y1 - 1
            dxx, dyy = abs(xx - x2), abs(yy - y2)
            if dxx == dyy:
                x_cord, y_cord, size, n_iter = x1 + 1, y1 - 1, dyy + 1, 2
            elif dx == dy:
                x_cord, y_cord, size, n_iter = x1, y1, dy + 1, 2
            elif dx > dy:
                x_cord, y_cord, size, n_iter = x2 - dy, y2 - dy, dy + 1, 1
            else:
                x_cord, y_cord, size, n_iter = x2 - dx, y2 - dx, dx + 1, 1

    else:
        # Reverse direction
        if dy == 0:
            if dx < abs(y2 - shape):
                x_cord, y_cord, size, n_iter = x2, y2, dx + 1, 1
            else:
                x_cord, y_cord, size, n_iter = x2, y2, abs(y2 - shape), 1

        elif dx == 0:
            if dy < abs(x1 - shape):
                x_cord, y_cord, size, n_iter = x1, y1, dy + 1, 1
            else:
                x_cord, y_cord, size, n_iter = x1, y2 - abs(x1 - shape) + 1, abs(x1 - shape), 1

        elif dy == 1 and dx != 1:
            x_cord, y_cord, size, n_iter = x2, y2 - 1, 2, 1

        else:
            if dx == dy:
                x_cord, y_cord, size, n_iter = x2, y1, dy + 1, 2
            elif dy < abs(x2 - shape):
                x_cord, y_cord, size, n_iter = x2, y2 - dy, dy + 1, 1
            else:
                x_cord, y_cord, size, n_iter = x2, y2 - abs(x2 - shape) + 1, abs(x2 - shape), 1

    return x_cord, y_cord, size, n_iter

def select_dynamic_block_columns(x1,y1,x2,y2,board):
    x_cord,y_cord,size, n_iterations = 1,1,1,1
    shape = board.shape[0]
    dx = abs(x1-x2)
    dy = abs(y1-y2)
    min_iter = float('inf')
    if y1 < y2:
        xx, yy = x1 + 1, y1 + 1
        dxx, dyy = abs(xx - x2), abs(yy - y2)
        if dxx == dyy and 2 < min_iter:
            min_iter = 2
            x_cord,y_cord,size,n_iterations = (x2, yy, dyy + 1, 2)
        elif dxx == 0 and dyy < abs(x2-shape) and 3 <= min_iter:
            min_iter = 3
            x_cord, y_cord, size, n_iterations = (x2-1, yy, dyy + 1, 3)
        elif dyy == 0 and dxx < abs(y2 - shape) and 1 < min_iter:
            min_iter = 1
            x_cord, y_cord, size, n_iterations = (x2, yy, dxx + 1, 1)

        if min_iter != float('inf'):
            return x_cord, y_cord, size, n_iterations
        

        if dx == 0:
            if dy < x1:
                x_cord,y_cord,size,n_iterations = (x2-dy,y1,dy+1,3)
            else:
                x_cord,y_cord,size,n_iterations = (0,y2-x1,x1+1,3)
        elif dx == 1 and x2 > x1:
            x_cord,y_cord,size,n_iterations = (x2-1,y2-1,2,1)
        else:
            xx = x1+1
            yy = y1+1
            if abs(xx-x2) == abs(yy-y2):
                x_cord,y_cord,size,n_iterations = (x2,y1+1,abs(yy-y2)+1,2)
            else:
                if dx == dy:
                    x_cord,y_cord,size,n_iterations = (x2,y1,dy+1,2)
                if dx > dy:
                    x_cord,y_cord,size,n_iterations = (x2,y2-dy,dy+1,2)
                if dx < dy:
                    x_cord, y_cord, size, n_iterations = (x2,y2-dx,dx+1,2)
    else:
        if dy == 0:
            if dx < abs(y2-shape):
                x_cord,y_cord,size,n_iterations = (x2,y2,dx+1,1)
            else:
                x_cord,y_cord,size,n_iterations = (x2,y2,abs(y2-shape),1)
        elif dx == 0:
            if dy < x1:
                x_cord,y_cord,size,n_iterations = (x2-dy,y2,dy+1,1)
            else:
                x_cord,y_cord,size,n_iterations = (0,y2,x1,1)
        elif dy == 1 and dx != 1:
            x_cord,y_cord,size,n_iterations = (x2,y2-1,2,1)
        else:
            if dx == dy:
                x_cord, y_cord, size, n_iterations = (x2,y2,dy+1,2)
            else:
                if dx < abs(y2-shape):
                    x_cord,y_cord,size,n_iterations = (x2,y2,dx+1,1)
                else:
                    x_cord,y_cord,size,n_iterations = (x2,y2, abs(y2-shape),1)
    
    return (x_cord,y_cord,size, n_iterations)


def solver_optimal(board, paired, ops, r=0):
    shape = board.shape[0]
    if shape < 2:
        return board, ops
    for i in range(0, 2):
        for j in range(shape-1):
            if paired[i][j] == True:
                continue

            ii, jj = find_partner(i, j, board, paired)
            dist = cal_distance(i,j,ii,jj)
            i2 = i+1
            j2 = j
            while dist > 1:
                x_cord,y_cord,size,n_iter = select_dynamic_block_rows(j2,i2,jj,ii,board)
                board = rotate90(x_cord,y_cord,size,n_iter,board,ops,r)
                ii,jj = find_positions(i,j,board)
                dist = cal_distance(i,j,ii,jj)

            if abs(ii - i) == 1 and abs(jj-j) == 0:
                board = rotate90(j, i, 2, 1, board, ops, r)
            
            ii, jj = find_positions(i, j, board)
            paired[i][j] = True
            paired[ii][jj] = True

    for j in range(shape-1, shape-3, -1):
        for i in range(2,shape):
            if paired[i][j] == True:
                continue

            ii, jj = find_partner(i, j, board, paired)
            dist = cal_distance(i,j,ii,jj)
            i2 = i
            j2 = j-1
            # print(f"Current value {board}")
            while dist > 1:
                x_cord,y_cord,size,n_iter = select_dynamic_block_columns(j2,i2,jj,ii,board)
                # print(x_cord,y_cord,size,n_iter)
                board = rotate90(x_cord,y_cord,size,n_iter,board,ops, r)
                ii,jj = find_positions(i,j,board)
                dist = cal_distance(i,j,ii,jj)
            if abs(ii - i) == 0 and abs(jj-j) == 1:
                board = rotate90(j-1,i,2, 1,board, ops, r)
            ii, jj = find_positions(i, j, board)
            paired[i][j] = True
            paired[ii][jj] = True

    if shape == 4:
        for i in range(shape-2,shape):
            for j in range(shape-1, -1, -1):
                if paired[i][j] == True:
                    continue

                ii, jj = find_partner(i, j, board, paired)
                dist = cal_distance(i,j,ii,jj)

                while dist > 1:
                    if abs(ii-i) == 1 and abs(jj-j) == 1:
                        board = rotate90(j-1,i-1,2,3,board,ops,r)
                        board = rotate90(j,i-1,3,3,board,ops,r)
                        board = rotate90(j-1,i-1,2,1,board,ops,r)
                        break

                ii, jj = find_positions(i, j, board)
                paired[i][j] = True
                paired[ii][jj] = True

    return solver_optimal(board[2:,:-2],paired[2:, :-2],ops, r+2)

# if __name__ == "__main__":
#     # board = np.array([[0,0,1,2,209,209,198,175,175,163,151,139,125,114,102,91,66,283,228,252,3,3,16,17],[18,18,1,2,224,199,199,176,176,163,151,139,115,115,102,91,67,283,227,252,4,4,24,17],[25,25,253,253,210,210,187,187,177,164,140,140,116,116,92,92,68,282,238,238,5,5,38,38],[39,40,239,239,225,211,188,188,177,164,141,141,117,117,93,93,69,282,237,237,6,6,53,53],[39,256,284,284,225,211,200,178,178,152,152,126,126,103,103,94,70,274,236,251,19,7,62,63],[64,247,276,265,78,34,34,258,229,216,215,214,228,227,226,226,71,281,236,250,19,7,221,63],[76,257,51,75,89,33,50,262,274,273,273,272,260,271,259,270,72,281,235,235,20,8,207,85],[86,258,59,59,101,33,49,121,132,144,156,170,181,193,203,217,73,272,224,249,20,8,185,100],[86,248,50,74,113,32,32,120,132,144,155,169,180,192,202,216,79,287,234,234,21,9,185,109],[110,259,49,74,113,22,48,120,131,131,155,169,180,192,202,215,79,271,223,248,22,9,160,109],[124,249,58,58,137,21,47,119,130,130,154,168,168,191,191,214,80,286,233,233,10,10,160,134],[135,260,48,257,241,240,55,66,67,68,69,70,71,72,73,213,81,270,232,232,11,11,149,147],[148,250,47,278,277,287,78,40,77,208,197,186,161,161,137,213,81,280,221,247,12,12,136,147],[148,251,57,278,277,276,90,64,89,29,29,30,30,31,31,212,275,206,231,231,23,13,111,172],[173,261,57,255,254,266,90,76,101,43,44,44,45,46,46,212,28,42,41,26,23,13,111,172],[173,261,45,255,254,242,114,87,112,275,263,104,118,118,119,104,28,27,27,26,14,14,88,195],[196,262,56,243,243,242,125,87,112,99,106,127,127,128,129,94,222,60,36,36,15,15,88,195],[196,263,56,230,218,229,138,110,136,99,105,142,143,128,129,207,222,61,37,37,24,16,77,219],[220,264,43,204,218,217,138,124,150,80,105,142,143,153,154,184,184,206,51,35,65,65,54,219],[220,264,55,204,194,203,162,135,150,98,98,165,166,153,167,208,223,52,52,35,42,41,54,245],[246,265,240,182,194,193,162,149,174,97,97,165,166,179,167,156,133,133,121,106,82,82,75,245],[246,266,241,182,171,181,186,159,174,96,96,189,189,179,190,145,145,122,122,107,83,83,60,267],[268,256,269,157,171,170,198,159,197,95,95,200,201,201,190,157,146,123,123,107,84,84,61,279],[268,286,269,280,285,279,267,244,244,230,205,205,183,183,158,158,146,134,108,108,100,85,62,285]])
#     # board = np.array([[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,16],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,1],[98,98,105,105,70,70,73,73,17,17,107,107,0,0,90,90],[54,54,127,127,85,85,118,118,112,112,110,110,108,108,20,20],[92,92,51,51,123,123,60,60,68,68,40,40,26,26,56,56],[78,78,124,124,99,99,37,37,47,47,109,109,116,116,36,36],[46,46,121,121,42,42,52,52,95,95,34,34,86,86,93,93],[31,31,83,83,81,81,101,101,53,53,58,58,117,117,19,19],[126,126,62,62,89,89,64,64,33,33,22,22,63,63,44,44],[125,125,119,119,38,38,102,102,25,25,23,23,120,120,41,41],[61,61,50,50,69,69,24,24,91,91,57,57,87,87,21,21],[67,67,114,114,113,113,28,28,30,30,79,79,96,96,65,65],[27,27,74,74,104,104,66,66,115,115,71,71,43,43,84,84],[111,111,29,29,75,75,59,59,55,55,88,88,100,100,80,80],[72,72,82,82,49,49,45,45,77,77,35,35,106,106,103,103],[32,32,48,48,39,39,94,94,18,18,76,76,122,122,97,97]])
#     # board = np.array([[16,4,47,28,22,67,56,52,54,48,2,70],[64,27,58,55,62,31,40,62,33,51,7,45],[1,59,10,71,64,18,21,0,19,15,60,5],[42,23,34,69,45,16,7,49,41,38,42,17],[15,59,13,26,25,43,44,36,53,23,60,32],[14,17,20,5,50,33,66,43,61,34,57,21],[54,70,47,66,39,20,13,30,8,48,12,52],[29,68,44,1,63,6,51,65,3,28,0,40],[67,18,56,69,71,38,26,46,9,41,68,39],[49,63,37,10,58,30,57,19,50,9,24,61],[29,12,65,55,11,32,31,3,11,2,6,8],[46,22,24,4,36,53,27,14,35,37,25,35]])
#     # board = np.array([[27,32,59,11,69,54,16,49,30,16,34,8],[26,70,51,71,65,12,6,40,67,58,62,66],[10,13,27,24,57,0,21,4,52,69,19,29],[40,25,17,8,53,65,5,15,15,21,31,24],[18,23,47,39,35,61,55,9,62,7,42,38],[61,58,68,14,33,63,5,60,25,49,43,59],[48,70,38,54,64,44,30,10,14,0,66,42],[11,67,37,20,22,7,36,50,32,60,29,28],[48,64,52,34,35,46,56,20,53,17,33,44],[39,28,12,47,56,26,2,45,4,50,41,13],[1,36,3,9,68,57,6,46,37,45,18,19],[3,1,31,51,2,23,43,55,41,22,63,71]])
#     # board = np.array([[3,49,49,8,48,16,20,24,34,61,50,11],[0,65,15,19,12,17,6,33,40,51,54,11],[31,47,64,63,60,13,52,55,53,38,30,45],[9,39,58,1,66,35,43,14,1,22,54,65],[0,66,36,67,53,27,7,42,8,59,21,13],[57,68,21,29,18,20,25,68,70,35,2,47],[69,5,67,46,62,4,32,25,23,71,15,59],[23,5,9,27,50,2,40,10,64,12,24,44],[7,71,38,17,70,14,51,16,37,26,43,41],[6,52,18,39,28,62,29,44,34,31,30,37],[58,28,56,19,55,45,69,3,46,41,10,56],[33,26,32,4,60,63,36,61,42,22,57,48]])
#     # board = np.array([[37,20,50,38,17,6,32,23,12,17,60,53],[54,41,21,56,10,62,71,47,24,38,5,11],[60,57,35,68,23,15,67,19,51,65,19,46],[66,49,18,66,59,40,64,30,15,41,16,22],[21,70,12,67,33,14,58,26,51,57,13,24],[47,27,69,58,59,69,20,63,64,52,45,68],[61,9,39,13,44,40,35,7,4,36,44,33],[11,39,31,2,62,29,30,18,37,61,53,27],[3,48,46,54,7,8,34,43,63,55,31,34],[28,43,56,14,25,48,45,50,65,28,0,32],[8,42,5,26,1,36,6,70,71,0,49,42],[52,16,10,55,3,25,9,2,29,1,22,4]])
#     shape = board.shape[0]
#     ops = []
#     paired = np.full((shape,shape), False, dtype=bool)
#     new_board, ops = solver_optimal(board, paired, ops, 0)
    
#     print(f"Number of step: {len(ops)}")
#     print("Success!")
#     with open("answer.json", "w") as f:
#         json.dump(ops, f)
#     # print(new_board)
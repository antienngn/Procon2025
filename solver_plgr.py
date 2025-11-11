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


# def select_dynamic_block_rows(x1,y1,x2,y2,board):
#     x_cord,y_cord,size, n_iterations = 1,1,1,1
#     shape = board.shape[0]
#     dx = abs(x1-x2)
#     dy = abs(y1-y2)
#     min_iterations = 10
#     if x1 < x2:
#         xx = x1+1
#         yy = y1-1
#         dxx = abs(xx-x2)
#         dyy = abs(yy-y2)
#         if dxx == dyy:
#             if 2 < min_iterations:
#                 min_iterations = 2
#                 x_cord,y_cord,size,n_iterations = (x1+1,y1-1,abs(yy-y2)+1,2)
#         elif dxx == 0 and dyy < abs(x2-shape):
#             if 1 < min_iterations:
#                 min_iterations = 1
#                 x_cord,y_cord,size,n_iterations = (xx,yy,dyy+1,1)
#         elif dyy == 0 and dxx < abs(y2-shape):
#             if 3 < min_iterations:
#                 min_iterations = 3
#                 x_cord,y_cord,size,n_iterations = (xx,yy,dxx+1,3)
#         if min_iterations != 10:
#             return x_cord, y_cord, size, n_iterations

#         if dy == 0:
#             if dx < abs(y2-shape):
#                 x_cord,y_cord,size,n_iterations = (x1,y1,dx+1,3)
#             else:
#                 x_cord,y_cord,size,n_iterations = (x2-abs(y2-shape)+1,y1,abs(y2-shape),1)
#         elif dy == 1 and y2 < y1:
#             if abs(x2-x1+1) <= abs(y2-shape):
#                 x_cord,y_cord,size,n_iterations = (x1+1,y2,dx,3)
#             else: 
#                 x_cord,y_cord,size,n_iterations = (x2-abs(y2-shape)+1,y2,abs(y2-shape),3)
#         else:
#             xx = x1+1
#             yy = y1-1
#             dxx = abs(xx-x2)
#             dyy = abs(yy-y2)
#             if dxx == dyy:
#                 x_cord,y_cord,size,n_iterations = (x1+1,y1-1,abs(yy-y2)+1,2)
#             else:
#                 if dx == dy:
#                     x_cord, y_cord, size, n_iterations = (x1,y1,dy+1,2)
#                 if dx > dy:
#                     x_cord,y_cord,size,n_iterations = (x2-dy,y2-dy,dy+1,1)
#                 if dx < dy:
#                     x_cord, y_cord, size, n_iterations = (x2-dx,y2-dx,dx+1,1)
#     else:
#         if dy == 0:
#             if dx < abs(y2-shape):
#                 x_cord,y_cord,size,n_iterations = (x2,y2,dx+1,1)
#             else:
#                 x_cord,y_cord,size,n_iterations = (x2,y2,abs(y2-shape),1)
#         elif dx == 0:
#             if dy < abs(x1-shape):
#                 x_cord,y_cord,size,n_iterations = (x1, y1, dy+1,1)
#             else:
#                 x_cord,y_cord,size,n_iterations = (x1,y2-abs(x1-shape)+1,abs(x1-shape),1)
#         elif dy == 1 and dx != 1:
#             x_cord,y_cord,size,n_iterations = (x2,y2-1,2, 1)
#         else:
#             if dx == dy:
#                 x_cord, y_cord, size, n_iterations = (x2,y1,dy+1,2)
#             else:
#                 if dy < abs(x2-shape):
#                     x_cord,y_cord,size,n_iterations = (x2,y2-dy,dy+1, 1)
#                 else:
#                     x_cord,y_cord,size,n_iterations = (x2,y2-abs(x2-shape)+1, abs(x2-shape),1)
    
#     return (x_cord,y_cord,size, n_iterations)


"""
Task 1: Verify dynamic block for columns again - Done
Task 2: Process when cell can move directly to target - Hmm maybe not worth 
Task 3: Solution for special case (when anti clockwise few step) - Doingg
"""
def select_dynamic_block_columns(x1,y1,x2,y2,board):
    x_cord,y_cord,size, n_iterations = 1,1,1,1
    shape = board.shape[0]
    dx = abs(x1-x2)
    dy = abs(y1-y2)
    min_iter = float('inf')
    if y1 < y2:
        xx, yy = x1 + 1, y1 + 1
        dxx, dyy = abs(xx - x2), abs(yy - y2)

        # Check diagonal first
        if dxx == dyy and 2 < min_iter:
            min_iter = 2
            x_cord,y_cord,size,n_iterations = x2, yy, dyy + 1, 2
        elif dxx == 0 and dyy < abs(x2 - shape) and 3 < min_iter:
            min_iter = 3
            x_cord, y_cord, size, n_iterations = x2, yy, dyy + 1, 3
        elif dyy == 0 and dxx < abs(y2 - shape) and 1 < min_iter:
            min_iter = 1
            x_cord, y_cord, size, n_iterations = x2, yy, dxx + 1, 1

        if min_iter != float('inf'):
            return x_cord, y_cord, size, n_iterations
        

        if dx == 0:
            if dy < x1:
                x_cord,y_cord,size,n_iterations = (x2-dy,y1,dy+1,3)
            else:
                x_cord,y_cord,size,n_iterations = (0,y2-x1,x1+1,3)
        elif dx == 1 and x2 > x1:
            x_cord,y_cord,size,n_iterations = (x2-1,y2-1,2,1)
            # if abs(y2-y1+1) < x1:
            #     x_cord,y_cord,size,n_iterations = (x2-dy,y1+1,dy,3)
            # else:
            #     x_cord,y_cord,size,n_iterations = (0,y2-x2,x2,3)
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


def solver(board, paired, ops, r=0):
    """
    Using dynamic size to rotate (not yet optimal :) ) 
    """
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
                print(board, y_cord,x_cord)
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

            while dist > 1:
                x_cord,y_cord,size,n_iter = select_dynamic_block_columns(j2,i2,jj,ii,board)
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

    return solver(board[2:,:-2],paired[2:, :-2],ops, r+2)

if __name__ == "__main__":
    # board = np.array([[47,16,39,48,51,69,8,59,2,70,30,52],
    #                    [17,65,46,45,12,46,29,43,36,40,65,47],
    #                    [54,1,4,26,54,27,32,57,41,23,29,13],
    #                    [52,14,31,9,16,18,22,22,12,15,39,61],
    #                    [60,51,71,17,30,44,7,37,69,55,48,55],
    #                    [11,4,61,31,41,25,28,70,64,8,58,9],
    #                    [20,59,10,53,68,38,44,28,19,37,71,67],
    #                    [24,13,68,33,32,42,3,20,49,27,40,34],
    #                    [60,58,21,26,5,63,34,35,43,14,56,49],
    #                    [24,33,6,56,50,1,66,0,2,10,23,57],
    #                    [21,36,18,63,19,66,45,6,7,0,5,11],
    #                    [3,62,50,15,53,62,25,64,35,67,42,38]])
    # board = np.array([[5,5,7,2],[0,3,6,0],[4,7,2,4],[1,6,3,1]])
    # board = np.array([[46,33,18,16,34,11,57,52,63,48,62,41],[69,8,12,8,25,65,4,37,39,64,31,10],[14,25,39,37,36,20,5,34,66,68,35,67],[24,45,0,40,54,63,14,2,61,26,17,43],[55,58,15,22,49,47,23,27,60,9,35,17],[42,28,65,32,64,26,43,15,55,57,1,50],[27,53,41,45,6,30,16,9,71,54,44,49],[56,58,33,70,2,30,13,70,44,61,19,31],[59,69,10,29,38,29,36,59,38,40,3,62],[1,67,50,71,7,52,4,48,5,51,46,12],[20,42,66,18,0,47,68,11,21,7,24,3],[28,60,13,23,21,6,22,53,19,56,32,51]])
    # board = np.array([[69,68,157,98,57,88,158,58,152,149,6,25,82,75,78,11,62,136],[69,91,46,50,128,141,150,3,125,115,145,53,116,15,77,81,131,110],[78,20,39,56,63,72,31,139,104,111,10,18,58,91,4,84,49,159],[151,80,120,53,103,67,140,147,48,100,56,34,97,64,96,80,22,13],[112,90,19,6,87,23,98,71,65,114,79,55,147,92,129,105,52,110],[32,104,23,153,108,1,3,76,68,144,10,118,102,28,18,29,37,155],[130,33,153,96,102,60,54,43,73,117,72,26,9,123,45,85,17,145],[41,133,142,70,7,95,59,143,5,30,101,86,146,38,117,34,60,148],[61,107,75,155,17,132,138,154,92,2,40,41,12,131,135,8,38,113],[144,137,85,152,137,29,37,127,105,62,120,99,5,12,113,136,161,138],[156,95,64,106,108,146,81,16,103,130,54,119,122,107,67,94,121,118],[0,2,14,52,15,33,160,35,159,90,126,55,79,100,119,42,19,127],[66,101,66,86,70,149,82,93,40,47,22,59,57,63,51,97,124,65],[26,123,121,126,132,133,50,0,83,39,36,148,77,88,21,115,154,27],[134,16,128,74,28,9,20,158,74,31,42,124,160,27,150,44,116,135],[141,4,21,43,25,99,112,1,83,7,44,106,51,13,151,134,45,87],[71,161,14,89,129,36,109,32,48,84,114,11,109,156,30,93,89,35],[47,142,8,94,143,61,140,24,76,157,24,46,122,125,73,139,49,111]])
    board = np.array([[285,174,139,222,5,277,179,175,117,208,4,211,195,148,182,267,24,96,46,246,146,81,153,228],[55,148,215,278,25,207,166,61,167,226,76,75,170,62,59,248,198,151,133,59,196,95,111,62],[245,11,65,235,131,172,279,252,9,2,40,276,81,248,80,126,146,94,243,45,120,12,7,82],[278,240,139,33,264,84,140,159,125,54,282,170,96,275,116,161,188,20,160,169,168,272,176,188],[268,23,126,234,36,64,168,60,67,257,232,233,106,135,134,12,13,70,153,101,249,197,192,233],[245,150,190,284,71,123,53,24,2,219,78,251,23,179,265,210,38,122,204,238,206,218,86,49],[13,223,34,185,8,100,73,56,226,164,165,105,208,48,194,38,180,77,191,147,87,84,21,166],[1,267,219,227,98,186,157,85,180,17,10,141,212,196,266,231,229,30,63,37,262,286,230,163],[63,214,138,242,158,155,283,263,252,259,112,236,271,110,91,118,204,100,41,88,265,214,47,102],[266,99,250,234,206,122,87,165,14,31,273,28,244,98,158,97,115,135,145,262,47,15,205,186],[224,198,220,244,239,77,270,210,95,18,255,16,43,6,246,142,241,21,17,227,92,104,274,255],[147,64,91,187,209,163,253,119,69,207,185,109,103,110,167,137,92,71,46,40,263,123,173,181],[162,73,177,187,129,52,182,52,35,241,169,144,68,35,283,212,3,107,145,149,74,251,205,151],[276,27,284,268,51,102,202,281,51,94,121,117,85,60,209,26,29,249,50,270,61,103,144,130],[177,197,149,3,28,128,280,271,239,34,192,114,5,45,129,156,32,164,143,65,66,109,162,48],[287,218,221,37,154,259,155,88,157,193,237,90,223,80,160,50,79,83,19,124,172,31,105,269],[140,132,137,201,175,236,1,217,230,199,150,203,256,44,7,54,25,183,132,178,269,108,184,171],[250,42,211,237,224,0,79,191,287,104,193,189,111,136,260,225,4,238,72,220,171,280,195,286],[39,106,189,228,115,213,121,190,116,200,86,42,216,176,257,141,183,114,57,125,201,225,112,53],[70,273,136,58,202,120,9,75,76,260,32,26,107,74,159,194,69,124,254,240,127,231,178,131],[72,29,10,113,36,56,253,174,261,57,20,49,22,19,78,15,89,258,216,215,11,30,184,18],[44,43,247,101,279,281,108,39,134,277,127,243,173,222,203,6,181,130,89,200,221,161,41,128],[14,68,152,0,97,142,8,27,66,55,99,22,143,83,82,272,285,90,118,229,242,275,154,138],[33,282,213,199,235,152,264,254,93,156,133,256,67,247,113,119,232,274,261,258,16,93,217,58]])
    # board = np.array([[52,33,70,29,1,2,54,97,95,51,61,34,10,71],[20,35,37,96,65,46,47,11,20,30,72,35,70,48],[17,56,85,54,83,40,39,3,50,32,0,11,39,41],[79,25,51,6,26,36,37,41,83,63,69,31,57,22],[45,29,13,28,80,26,36,77,73,91,30,97,19,69],[38,55,27,46,84,9,92,45,94,87,64,5,13,84],[21,52,67,67,71,77,8,24,23,78,95,78,92,49],[15,16,25,12,81,14,74,44,89,68,0,93,18,17],[81,60,53,75,76,1,68,58,19,15,49,7,8,63],[91,32,47,75,55,10,73,62,7,4,43,89,22,24],[57,65,14,2,21,5,86,82,76,48,59,4,16,79],[88,62,86,23,43,80,31,50,44,34,6,42,60,88],[61,3,12,66,72,82,94,85,58,27,28,56,53,96],[9,33,38,66,90,90,93,64,74,87,18,40,42,59]])
    # board = np.array([[0,1,2,2,3,4,5,5,6,7,7,8],[0,1,9,10,3,4,11,12,6,13,14,8],[15,15,9,10,16,17,11,12,18,13,14,19],[20,21,21,22,16,17,23,23,18,24,25,19],[20,26,27,22,28,29,30,31,31,24,25,32],[33,26,27,34,28,29,30,35,36,36,37,32],[33,38,44,38,39,39,40,35,41,41,37,42],[43,43,44,34,45,46,40,47,48,48,49,42],[50,51,52,53,45,46,54,47,55,55,49,56],[50,51,52,53,57,58,58,59,66,60,61,56],[62,62,63,64,57,65,54,59,67,60,61,68],[69,69,63,64,70,70,65,71,66,67,71,68]])
    shape = board.shape[0]
    ops = []
    paired = np.full((shape,shape), False, dtype=bool)
    new_board, ops = solver(board, paired, ops, 0)
    print(f"Number of step: {len(ops)}")
    with open("answer.json", "w") as f:
        json.dump(ops, f)
    # print(new_board)
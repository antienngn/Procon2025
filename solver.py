import numpy as np
import json
from utils import rotate90, find_partner, check_distance, cal_distance, find_positions, select_dynamic_block

def solver(board):
    """
    Using 2x2 only to rotate
    """
    shape = board.shape[0]
    total_pairs = (shape*shape)//2
    paired = np.full((shape,shape), False, dtype=bool)
    score = 0
    ops = []
    while score < total_pairs:
        for i in range(shape):
            for j in range(shape):
                if paired[i][j] == True:
                    continue
                
                ii, jj = find_partner(i, j, board, paired)
                # if check_distance(i,j,ii,jj):
                #     if abs(ii - i) == 1 and abs(jj-j) == 0:
                #         board = rotate90(j, i, 2, board)
                #         ops.append({"x": j, "y": i, "n": 2})
                #     ii, jj = find_positions(i, j, board) 
                #     paired[i][j] = True
                #     paired[ii][jj] = True
                #     score += 1
                #     continue
                
                dist = cal_distance(i,j,ii,jj)
                print(len(ops))
                print(board)
                while dist > 1:
                    if jj > j:
                        if j >= shape-2 and i >= shape-2:
                            if abs(ii-i) == 1 and abs(jj-i) == 1:
                                board = rotate90(j,i-1,2,board,ops)
                                board = rotate90(j-2,i-1,3,board,ops)
                                board = rotate90(j,i-1,2,board,ops)
                                board = rotate90(j-2,i,2,board,ops)
                                board = rotate90(j,i,2,board,ops)
                                break
                        i2 = i
                        j2 = j + 1
                        x_cord,y_cord,size,n_iter = select_dynamic_block(j2,i2,jj,ii,board)
                        board = rotate90(x_cord,y_cord,size,n_iter,board, ops) 
                        # if (abs(ii-i) == 1 and abs(jj - j) > 1) or (abs(ii-i) > 1 and abs(jj-j) == 1) or (abs(ii-i) > 1 and abs(ii-i) > 1):
                        #     board = rotate90(jj-1, ii-1, 2, board, ops)
                        # elif (abs(ii-i) == 0 and abs(jj-j) > 1) or (abs(ii-i) == 1 and abs(jj-j) == 1 and jj == shape-1):
                        #     board = rotate90(jj-1, ii, 2, board, ops)
                        # elif abs(ii - i) == 1 and abs(jj - j) == 1 and jj < shape-1:
                        #     board = rotate90(jj, ii-1, 2, board, ops)
                    else:
                        i2 = i+1
                        j2 = j
                        x_cord,y_cord,size,n_iter = select_dynamic_block(j2,i2,jj,ii,board)
                        board = rotate90(x_cord,y_cord,size,n_iter,board, ops)
                        # if abs(ii-i) > 1:
                        #     board = rotate90(jj, ii-1, 2, board, ops)
                        # elif abs(ii-i) == 1 and abs(jj-j) >= 1:
                        #     board = rotate90(jj, ii, 2, board, ops)
                        # elif abs(ii-i) == 1 and abs(jj-j) == 0:
                        #     break
                    print(board)
                    # print(ii,jj)
                    ii,jj = find_positions(i,j,board)
                    dist = cal_distance(i,j,ii,jj)

                if check_distance(i,j,ii,jj):
                    if i < shape - 2:
                        if abs(ii - i) == 1 and abs(jj-j) == 0:
                            board = rotate90(j, i, 2, board, ops)
                        ii, jj = find_positions(i, j, board)
                        paired[i][j] = True
                        paired[ii][jj] = True
                        score += 1
                    else:
                        if abs(ii - i) == 0 and abs(jj-j) == 1:
                            count = 0
                            while count <= 2:
                                board = rotate90(j,i,2,board, ops)
                                count += 1  
                        ii, jj = find_positions(i, j, board)
                        paired[i][j] = True
                        paired[ii][jj] = True
                        score += 1
                
    return board, ops

if __name__ == "__main__":
    board = np.array([[47,16,39,48,51,69,8,59,2,70,30,52],
                       [17,65,46,45,12,46,29,43,36,40,65,47],
                       [54,1,4,26,54,27,32,57,41,23,29,13],
                       [52,14,31,9,16,18,22,22,12,15,39,61],
                       [60,51,71,17,30,44,7,37,69,55,48,55],
                       [11,4,61,31,41,25,28,70,64,8,58,9],
                       [20,59,10,53,68,38,44,28,19,37,71,67],
                       [24,13,68,33,32,42,3,20,49,27,40,34],
                       [60,58,21,26,5,63,34,35,43,14,56,49],
                       [24,33,6,56,50,1,66,0,2,10,23,57],
                       [21,36,18,63,19,66,45,6,7,0,5,11],
                       [3,62,50,15,53,62,25,64,35,67,42,38]])

    new_board, ops = solver(board)
    print(f"Number of step: {len(ops)}")
    with open("answer.json", "w") as f:
        json.dump(ops, f)
    print(new_board)
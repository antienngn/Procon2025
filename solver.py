import numpy as np
import json
import os
from utils import extract_entities, rotate90

file_path = "./Problem/problem.json"
key_feature = ["problem", "field", "entities"]

def solver():
    garden = extract_entities(file_path=file_path, key_feature=key_feature)
    rows, columns = garden.shape
    for i in rows:
        for j in columns:
            if garden[i][j] != garden[i+1][j+1]:
                rotate90(x_cord=0, y_cord=0, size=3, garden=garden)
    
    # print(temp)
    # return temp

def bfs():
    return        

if __name__ == "__main__":
    # print(np.array(extract_entities(file_path=file_path,key_feature=key_feature)))
    # print(solver())
    solver()
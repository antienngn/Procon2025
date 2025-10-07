import numpy as np
import json
import os
from utils import extract_entities, rotate90

file_path = "./Problem/problem.json"
key_feature = ["problem", "field", "entities"]

def solver():
    garden = extract_entities(file_path=file_path, key_feature=key_feature)
    print(garden,"\n")
    temp = rotate90(x_cord=0, y_cord=0, size=3, garden=garden)
    print(temp)
    # return temp

        

if __name__ == "__main__":
    # print(np.array(extract_entities(file_path=file_path,key_feature=key_feature)))
    # print(solver())
    solver()
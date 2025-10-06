import numpy as np
import json
import os
from utils import extract_entities

file_path = "./Problem/problem.json"
key_feature = ["problem", "field", "entities"]

def solver():
    garden = extract_entities(file_path=file_path, key_feature=key_feature)
    return garden

        

if __name__ == "__main__":
    # print(np.array(extract_entities(file_path=file_path,key_feature=key_feature)))
    # print(solver())
    solver()
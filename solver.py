import numpy as np
import json
import os

file_path = "./Problem/problem.json"
key_feature = ["problem", "field", "entities"]

def extract_entities(file_path, key_feature):
    try:
        with open(file_path, "r", encoding='utf-8') as f:
            data= json.load(f)
        current = data
        for key in key_feature:
            if key in current and isinstance(current, dict):
                current = current[key]
        problem = current
    except FileNotFoundError:
        print(f"File not found '{file_path}'.")

    return np.array(problem)

def solver():
    garden = extract_entities(file_path=file_path, key_feature=key_feature)
    return garden

        

if __name__ == "__main__":
    # print(np.array(extract_entities(file_path=file_path,key_feature=key_feature)))
    # print(solver())
    solver()
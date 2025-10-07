import json 
import numpy as np

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

def rotate90(x_cord, y_cord, size, garden):
    for x_cord in range(size):
        for y_cord in range(x_cord+1, size):
            garden[x_cord][y_cord], garden[y_cord][x_cord] = garden[y_cord][x_cord], garden[x_cord][y_cord]

    block = garden[x_cord:x_cord+size, y_cord:y_cord+size]
    for row in block:
        np.flip(row)
    
    return garden
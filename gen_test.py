import random
import json
import os
import numpy as np
from typing import List

def generate_matrix(N):
    if N < 2 or N > 24:
        raise ValueError("N in range 4 to 24")
    if (N * N) % 2 != 0:
        raise ValueError("Number must even!")

    num_pairs = (N * N) // 2
    
    entities = []
    for v in range(num_pairs):
        entities.append(v)
        entities.append(v)  

    random.shuffle(entities)
    field_matrix: List[List[int]] = []
    for r in range(N):
        start_index = r * N
        end_index = (r + 1) * N
        row = entities[start_index:end_index]
        field_matrix.append(row)

    return field_matrix

def generate_problem(N):
    template_json = {
        "startsAt": 0,
        "problem": {
            "field": {
                "size": N,
                "entities": generate_matrix(N)
            }
        }
    }
    save_dir = "./Problem"
    output_json = "problem.json"
    output_path = os.path.join(save_dir, output_json)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(f"Create directory: {save_dir}")
    try:
        with open(output_path, "w", encoding='utf-8') as f:
            json.dump(template_json, f, ensure_ascii=False, indent=4)
        print(f"Create json sucessful! at {output_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    #Number is even and in range 4 to 24    
    N = 12
    generate_problem(N)

    #Just check my code :)
    # mat = generate_matrix(N)
    # print(np.array(mat))
    # print(np.max(mat))
    # for i in range(np.max(mat)+1):
    #     count = np.sum(np.array(mat) == i)
    #     print(f"Element {i} has: {count} number")

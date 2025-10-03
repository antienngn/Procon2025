import random

def generate_matrix(N):
    if N < 2 or N > 24:
        raise ValueError("N phải nằm trong khoảng từ 2 đến 24")
    if (N * N) % 2 != 0:
        raise ValueError("Số phần tử trong ma trận phải là số chẵn để chia thành cặp")

    num_pairs = (N * N) // 2
    
    if num_pairs > 23:  
        raise ValueError("Không thể tạo ma trận vì số cặp vượt quá 23 (số giá trị khả dụng)")

    values = random.sample(range(2, 25), num_pairs)  
    paired_values = []
    for v in values:
        paired_values.extend([v, v])  

    random.shuffle(paired_values)

    matrix = [paired_values[i * N:(i + 1) * N] for i in range(N)]
    return matrix

if __name__ == "__main__":
    N = random.randint(2, 24)
    while (N * N) % 2 != 0 or (N * N) // 2 > 23:  
        N = random.randint(2, 24)

    print(f"Ma trận {N}x{N}:")
    mat = generate_matrix(N)
    for row in mat:
        print(row)

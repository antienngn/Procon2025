import requests
import json
import numpy as np
from solver_general_optimal import solver_optimal
from solver_special_fused import solver_hybrid
from utils import count_pairs

headers = {'Authorization': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjksIm5hbWUiOiJVRVQuY3VCTEFTIiwiaXNfYWRtaW4iOmZhbHNlLCJpYXQiOjE3NjM3Nzc0MTMsImV4cCI6MTc2Mzk1MDIxM30.WCHTHeTYasbS-rzn-NvexdgBAUlCJ0IBXqjecssEtWE"}
url = 'https://procon25-api.haiuet.me'

#Nhập id câu hỏi ở đây
qid = 120

r = requests.get(f'{url}/question/{qid}', headers=headers, verify=False)
# print(r.text)
# print(r.status_code)
question = r.json()
data = json.loads(question["question_data"])

entities = data["field"]["entities"]   
size      = data["field"]["size"]

board = np.array(entities)

ops = []
shape = board.shape[0]
paired = np.full((shape, shape), False, dtype=bool)

total_correct_pairs = (shape*shape)//2



# new_board,ops = solver_hybrid(board, ops)

new_board,ops = solver_optimal(board,paired,ops,0)

# print(f"Số lượng cặp: {count_pairs(new_board)}")
payload = {
  "question_id": qid,
  "answer_data": {
    "ops": ops
  }
}

print(f"Length step: {len(ops)}")

s = requests.post(f'{url}/answer', json=payload, headers=headers)

# print(s.text)

# p = requests.get(f'{url}/answer/3', json = payload, headers=headers)
# print(p.json()["score_data"])
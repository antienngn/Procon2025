import requests
import json

headers = {'Authorization': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NCwibmFtZSI6IkFWSCIsImlzX2FkbWluIjpmYWxzZSwiaWF0IjoxNzI1NjA5MTE2LCJleHAiOjE3MjU3ODE5MTZ9._e_lQifCjtuBlJSzeejWohbAtUHQ6gCq2fx_eSx26Bc"}
url = 'https://proconvn.duckdns.org'
qid = 68
r = requests.get(f'{url}/question/{qid}', headers=headers)


question = r.json()
data = json.loads(question["question_data"])
board = data["board"]
goal = board["goal"]
start = board["start"]
# print(start)
res, _ = row_cutting_best.transform_until_match(start, goal)

# ops = []
# for x in res:
#     item = {}
#     s = x[0]
#     if s == "right":
#         s = 3
#     if s == "left":
#         s = 2
#     if s == "up":
#         s = 0
#     if s == "down":
#         s = 1
#     item['s'] = s
#     item['p'] = x[2]
#     item['x'] = x[1][0]
#     item['y'] = x[1][1]
#     ops.append(item)

payload = {"question_id": qid, "answer_data": {"n": len(ops), "ops": ops}}

# print(len(ops))
# s = requests.post(f'{url}/answer', json=payload, headers=headers)

# print(s.text)

# p = requests.get(f'{url}/answer/3', json = payload, headers=headers)
# print(p.json()["score_data"])
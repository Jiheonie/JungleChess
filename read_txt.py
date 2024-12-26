result = []  
player = ""
with open('example.txt', 'r', encoding='utf-8') as file:
  lines = file.readlines()
  for line in lines[:-1]:
    parts = [item[0:2] for item in line.split("  ") if item]
    # result.append(parts)  
    result = parts + result
  player = lines[-1]

for i in range(len(result)):
  if result[i] == "EL":
    result[i] = [2, 8]
  elif result[i] == "LI":
    result[i] = [2, 7]
  elif result[i] == "TI":
    result[i] = [2, 6]
  elif result[i] == "LE":
    result[i] = [2, 5]
  elif result[i] == "DO":
    result[i] = [2, 4]
  elif result[i] == "WO":
    result[i] = [2, 3]
  elif result[i] == "CA":
    result[i] = [2, 2]
  elif result[i] == "RA":
    result[i] = [2, 1]

  elif result[i] == "el":
    result[i] = [1, 8]
  elif result[i] == "li":
    result[i] = [1, 7]
  elif result[i] == "ti":
    result[i] = [1, 6]
  elif result[i] == "le":
    result[i] = [1, 5]
  elif result[i] == "do":
    result[i] = [1, 4]
  elif result[i] == "wo":
    result[i] = [1, 3]
  elif result[i] == "ca":
    result[i] = [1, 2]
  elif result[i] == "ra":
    result[i] = [1, 1]

  else:
    result[i] = [0, 0]

board = [[0, 0] for _ in range(63)] 
power = [result[i][1] for i in range(63)]
for r in range(9):
  for c in range(7):
    idx = r * 7 + c
    if (r == 0 and (c == 2 or c == 4)) or (r == 1 and c == 3):
      board[idx] = [1, 2]
      if result[idx][0] == 2:
        power[idx] = 0
    elif r == 0 and c == 3:
      board[idx] = [1, 1]
    elif (r == 8 and (c == 2 or c == 4)) or (r == 7 and c == 3):
      board[idx] = [2, 2]
      if result[idx][0] == 1:
        power[idx] = 0
    elif r == 8 and c == 3:
      board[idx] = [2, 1]
    elif r in range(3, 6) and (c in range(1, 3) or c in range(4, 6)):
      board[idx] = [0, 3]
    else:
      board[idx] = [0, 4]
    result[idx] = board[idx] + [result[idx][0], power[idx], result[idx][1]]


print(result)
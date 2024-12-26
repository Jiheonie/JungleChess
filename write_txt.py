import numpy as np
import os
import time
import argparse
import h5py
from dljungle.kerasutil import load_model_from_hdf5_group


def encode_from_txt(file):
  result = []  
  player = ""
  with open(file, 'r', encoding='utf-8') as file:
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

  if player == "bl":
    p = 1
  else:
    p = 2

  return result, p


def write_to_txt(moves, outfile):
  contents = []
  for move in moves:
    r = move[0] // 7
    r = 8 - r
    c = move[0] % 7

    first_idx = r * 7 + c
    if move[1] == 0:
      second_idx = first_idx - 7
    elif move[1]  == 1:
      second_idx = first_idx + 1
    elif move[1] == 2:
      second_idx = first_idx + 7
    else:
      second_idx = first_idx - 1
    
    contents.append(f"{first_idx} {second_idx}\n")

  with open(outfile, 'w', encoding='utf-8') as file:
    for c in contents:
      file.write(c)


def load_model(h5file):
  model = load_model_from_hdf5_group(h5file['model'])
  return model


def predict(model, board):
  board = np.reshape(board, (1, 9, 7, 5))
  move_probs = model.predict(board)[0]
  print(move_probs)
  num_moves = 9 * 7 * 4
  candidates = np.arange(num_moves)
  moves = np.random.choice(candidates, num_moves, replace=False, p=move_probs)

  result = []
  for idx in moves:
    point = idx // 4
    direc = idx % 4
    r = point // 7
    c = point % 7 
    # if board[0, r, c, 2] == player and moves[idx] > max_val:
    #   max_idx = idx
    #   max_val = moves[idx]
    #   # return [point, direc]
    result.append([point, direc])
  return result

def get_file_modification_time(file_path):
    return os.path.getmtime(file_path)

def main():
  file_path = 'example.txt'
  model = load_model(h5py.File('agents/policy_agent_2.hdf5'))

  print(f"Start monitoring {file_path}. Waiting for changes...")
  last_mod_time = get_file_modification_time(file_path)

  while True:
    current_mod_time = get_file_modification_time(file_path)

    if current_mod_time != last_mod_time:
      board, player = encode_from_txt(file_path)
      move = predict(model, np.array(board))
      write_to_txt(move, 'write_ex.txt')
      last_mod_time = current_mod_time



if __name__ == "__main__":
  main()
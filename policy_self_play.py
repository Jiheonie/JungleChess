import argparse
import datetime

import h5py
from dljungle.rl.experience import ExperienceCollector, combine_experience
from dljungle.jungleBoard import GameState, Board
from dljungle.jungleTypes import Player, Square, Point, ChessType
from dljungle.utils import custom_board, print_board
from dljungle.agent.pg import load_policy_agent
from dljungle.agent.helpers import is_move_valid

def get_position_value(chess, r, c):
  if chess.player == Player.GREEN:
    if r <= 6:
      return 1
    control_cave = [[7, 4], [8, 3], [8, 5], [9, 2], [9, 6]]
    for pair in control_cave:
      if r == pair[0] and c == pair[1]:
        return 3
    cave = [[8, 4], [9, 3], [9, 5]]
    for pair in cave:
      if r == pair[0] and c == pair[1]:
        return 4
    return 2
  
  if r >= 4:
    return 1
  control_cave = [[3, 4], [2, 3], [2, 5], [1, 2], [1, 6]]
  for pair in control_cave:
    if r == pair[0] and c == pair[1]:
      return 3
  cave = [[2, 4], [1, 3], [1, 5]]
  for pair in cave:
    if r == pair[0] and c == pair[1]:
      return 4
  return 2



def capture_diff(game_state):
  gp = 0
  rp = 0
  g_position = 0
  r_position = 0

  gsum = 0
  rsum = 0

  g_threat = 0
  r_threat = 0

  w1 = 10
  w2 = 3
  w3 = 5

  for r in range(1, 10):
    for c in range(1, 8):
      point = Point(r, c)
      square = Square.get_by_point(point)
      chess = game_state.board.get_chess_by_point(point)

      if chess:
        chess_value = chess.chesstype.value if isinstance(chess.chesstype, ChessType) else 0

        if chess.player == Player.GREEN:
          gp += chess.lost_power.value
          g_position += get_position_value(chess, r, c)

          for di in point.neighbors():
            if is_move_valid(chess.player, game_state.board, square, di):
              gp += 1
            dest_chess = game_state.board.get_chess_by_point(point.neighbors()[di])
            if dest_chess:
              dest_chess_value = dest_chess.chesstype.value if isinstance(dest_chess.chesstype, ChessType) else 0
              if dest_chess.player == Player.RED and dest_chess_value <= chess_value:
                g_threat += dest_chess.lost_power.value
          

        else:
          rp += chess.lost_power.value
          r_position += get_position_value(chess, r, c)

          for di in point.neighbors():
            if is_move_valid(chess.player, game_state.board, square, di):
              rp += 1
            dest_chess = game_state.board.get_chess_by_point(point.neighbors()[di])
            if dest_chess:
              dest_chess_value = dest_chess.chesstype.value if isinstance(dest_chess.chesstype, ChessType) else 0
              if dest_chess.player == Player.GREEN and dest_chess_value <= chess_value:
                r_threat += dest_chess.lost_power.value

  gsum = gp * w1 + g_position * w2 + g_threat * w3
  rsum = rp * w1 + r_position * w2 + r_threat * w3

  diff = gsum - rsum
  if diff >= 0:
    return Player.GREEN
  return Player.RED

def simulate_game(green, red):
  moves = []

  board = Board()
  custom_board(board=board)
  print_board(board=board)
  game = GameState.new_game(board=board)
  agents = {
    Player.GREEN: green,
    Player.RED: red
  }

  num_moves = 0

  # while not game.is_over() and num_moves < 100:
  while not game.is_over():
    next_move = agents[game.next_player].select_move(game)
    moves.append(next_move)
    game = game.apply_move(next_move)
    num_moves += 1

  print_board(board=game.board)

  # if num_moves == 100:
  #   return capture_diff(game_state=game)

  return game.winner


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--learning-agent', required=True)
  parser.add_argument('--num-games', type=int, default=10)
  parser.add_argument('--experience-out', required=True)

  args = parser.parse_args()
  agent_filename = args.learning_agent
  experience_filename = args.experience_out
  num_games = args.num_games

  agent1 = load_policy_agent(h5py.File(agent_filename))
  agent2 = load_policy_agent(h5py.File(agent_filename))
  collector1 = ExperienceCollector()
  collector2 = ExperienceCollector()
  agent1.set_collector(collector1)
  agent2.set_collector(collector2)

  for i in range(args.num_games):
    print('Simulating game %d/%d...' % (i + 1, args.num_games))
    collector1.begin_episode()
    collector2.begin_episode()

    winner = simulate_game(agent1, agent2)
    if winner == Player.GREEN:
      collector1.complete_episode(reward=1)
      collector2.complete_episode(reward=-1)
    else:
      collector2.complete_episode(reward=1)
      collector1.complete_episode(reward=-1)

  experience = combine_experience([collector1, collector2])
  with h5py.File(experience_filename, 'w') as experience_outf:
    experience.serialize(experience_outf)


if __name__ == '__main__':
  main()
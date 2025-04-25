from cube import Cube
from model import IDAStar
from cost import Cost

import os
import json
import time
import argparse

parser = argparse.ArgumentParser(description="Solve a Rubik's Cube using IDA* algorithm.")
parser.add_argument("--size", type=int, default=3, help="Size of the Rubik's Cube (default: 3).")
parser.add_argument("--threshold", type=int, default=20, help="Maximum search depth for heuristic generation (default: 20).")
parser.add_argument("--shuffle_lower_bound", type=int, default=1, help="Lower bound for shuffle moves (default: 1).")
parser.add_argument("--shuffle_upper_bound", type=int, default=5, help="Upper bound for shuffle moves (default: 5).")

args = parser.parse_args()

db_directory = f"./database/cube_{args.size}x{args.size}x{args.size}/"
db_file_path = db_directory + "heuristic.json"

if not os.path.exists(db_directory):
    os.makedirs(db_directory)

heuristic = None
if os.path.exists(db_file_path):
    with open(db_file_path, "r") as f:
        heuristic = json.load(f)

if heuristic is None:
    print("Heuristic not found, building database...")
    cost = Cost(n=args.size, max_depth=5)
    heuristic = cost.heuristic
    with open(db_file_path, "w") as f:
        json.dump(heuristic, f, ensure_ascii=False, indent=4)

model = IDAStar(threshold=args.threshold, heuristic=heuristic)

cube = Cube(n=args.size)

moves = cube.shuffle(args.shuffle_lower_bound, args.shuffle_upper_bound)

n = len(moves)
print(f"Shuffled state: {cube.state}")

moves = "\n" + "\n".join([f"{move[0]}" for move in moves])
print(f"Shuffled in {n} moves: {moves}")

s = time.perf_counter_ns()
moves = model.solve(cube.state)
e = time.perf_counter_ns()

n = len(moves)
if moves:
    final_state = moves[-1][1]
final_state = Cube(n=args.size).state

moves = "\n" + "\n".join([f"{move[0]}" for move in moves])
print(f"Solved in {n} in {(e-s)/1e6:.3f} ms with moves: {moves}")

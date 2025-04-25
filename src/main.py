from cube import Cube
from model import IDAStar
from cost import Cost

import os
import json
import time

db_file = "./heuristic.json"

heuristic = None
if os.path.exists(db_file):
    with open(db_file, "r") as f:
        heuristic = json.load(f)

if heuristic is None:
    print("Heuristic not found, building database...")
    cost = Cost(max_depth=5)
    heuristic = cost.heuristic
    with open(db_file, "w") as f:
        json.dump(heuristic, f, ensure_ascii=False, indent=4)

model = IDAStar(threshold=5, heuristic=heuristic)

cube = Cube()
moves = cube.shuffle(1, 5)
print(f"Shuffled state: {cube.state}")
print(f"Shuffled in {len(moves)} moves: {[move[0] for move in moves]}")

s = time.perf_counter_ns()
moves = model.solve(cube.state)
e = time.perf_counter_ns()

print(f"Solved in {len(moves)} moves: {[move[0] for move in moves]} in {(e-s):,} ns")
print(f"Solved state: \t{moves[-1][1]}")

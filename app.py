from flask import Flask, render_template, request, redirect, url_for

from src.cube import Cube
from src.cost import Cost
from src.model import Model, IDAStar

import os
import json

app = Flask(__name__)

DEFAULT_SIZE = 3
DEFAULT_MAX_DEPTH = 5
DEFAULT_LOWER_STEP_LIMIT = 1
DEFAULT_UPPER_STEP_LIMIT = 5

cube = None

@app.route('/', methods=['GET', 'POST'])
def index():
    default_size = DEFAULT_SIZE

    if request.method == 'POST':
        size = int(request.form.get('size', default_size))

        if size < 1 or size > 6:
            print("Error: Cube size too large.")
            return render_template('index.html', error="Cube size out of bounds. Choose a size between 1 and 6.")
        
        global cube
        cube = Cube(n=int(size))
        return render_template('index.html', size=size, cube=cube)
    
    return render_template('index.html')

@app.route('/solve', methods=['GET', 'POST'])
def solve():
    if request.method == 'GET':
        return redirect(url_for('index'))

    global cube
    if cube is None:
        return redirect(url_for('index'))
    
    size = cube.n
    steps_low = int(request.form.get('lower-limit', DEFAULT_LOWER_STEP_LIMIT))
    steps_high = int(request.form.get('upper-limit', DEFAULT_UPPER_STEP_LIMIT))

    if steps_low < 1 or steps_high > 10 or steps_low > steps_high:
        print("Error: Number of steps out of bounds.")
        return render_template('index.html', error="Number of steps out of bounds. Choose a number between 1 and 10.")
    
    shuffle_moves = cube.shuffle(steps_low, steps_high)

    db_directory = f"./database/cube_{size}x{size}x{size}/"
    db_file_path = db_directory + f"heuristic.json"

    if not os.path.exists(db_directory):
        os.makedirs(db_directory)

    heuristic = None
    if os.path.exists(db_file_path):
        with open(db_file_path, "r") as f:
            heuristic = json.load(f)

    if heuristic is None:
        print("Heuristic not found, building database...")
        cost = Cost(n=size, max_depth=DEFAULT_MAX_DEPTH)
        heuristic = cost.heuristic
        with open(db_file_path, "w") as f:
            json.dump(heuristic, f, ensure_ascii=False, indent=4)

    model = IDAStar(heuristic=heuristic)
    solve_moves = model.solve(cube.state)

    return render_template('solve.html', size=size, cube=cube, shuffle_moves=shuffle_moves, solve_moves=solve_moves)

if __name__ == '__main__':
    app.run(debug=True)

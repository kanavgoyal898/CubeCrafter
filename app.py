from flask import Flask, render_template, request, redirect, url_for

from src.cube import Cube
from src.cost import Cost
from src.model import Model, IDAStar

app = Flask(__name__)

DEFAULT_SIZE = 3
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

    if steps_low < 1 or steps_high > 100 or steps_low > steps_high:
        print("Error: Number of steps out of bounds.")
        return render_template('solve.html', error="Number of steps out of bounds. Choose a number between 1 and 100.")
    
    shuffle_moves = cube.shuffle(steps_low, steps_high)
    print(f"Shuffled in {len(shuffle_moves)} moves.")

    return render_template('solve.html', size=size, cube=cube, shuffle_moves=shuffle_moves)

if __name__ == '__main__':
    app.run(debug=True)

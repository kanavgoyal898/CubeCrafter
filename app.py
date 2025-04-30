from flask import Flask, render_template, request

from src.cube import Cube
from src.cost import Cost
from src.model import Model, IDAStar

app = Flask(__name__)

DEFAULT_SIZE = 3

@app.route('/', methods=['GET', 'POST'])
def index():
    default_size = DEFAULT_SIZE
    if request.method == 'POST':
        size = int(request.form.get('size', default_size))
        cube = Cube(n=int(size))
        return render_template('index.html', default_size=default_size, size=size, cube=cube)
    return render_template('index.html', cube=None)

if __name__ == '__main__':
    app.run(debug=True)

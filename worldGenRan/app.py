from flask import Flask, render_template
import mapGen

app = Flask(__name__)

@app.route('/')
def home():
    # Generate the world grid
    world_grid = mapGen.SetworldGrid()
    # Pass the world grid to the HTML template
    return render_template('index.html', world_grid=world_grid)

if __name__ == '__main__':
    app.run()

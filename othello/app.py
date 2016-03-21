from flask import Flask
from flask import render_template
app = Flask(__name__)
from game import Game

@app.route("/")
def hello():
    return "Hello World!"

def play_point():
	return

game = Game()

@app.route("/view_game")
def view_game():
	print(game.board_size)
	return render_template('board.html.j2', game=game)

if __name__ == "__main__":
    app.run(debug=True)
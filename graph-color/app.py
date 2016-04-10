from flask import Flask, render_template
import pygal
from pygal.style import NeonStyle
import random
import math

app = Flask(__name__)

@app.route("/")
def hello():
  return render_template("hello.html.j2")

@app.route("/chart.svg")
def chart():
  chart = pygal.XY(dots_size=10, stroke=False, explicit_size=True, width=500, height=500)

  xy_points = [y for y in zip(random_k(5), random_k(5))]
  chart.add('Nodes', xy_points)
  return chart.render_response()

if __name__ == "__main__":
    app.run(debug=True)
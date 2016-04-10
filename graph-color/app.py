from flask import Flask, render_template
import pygal
from pygal.style import NeonStyle
import random
import math
import graphs

app = Flask(__name__)

@app.route("/")
def hello():
  return render_template("hello.html.j2")

@app.route("/chart.svg")
def chart():
  chart = pygal.XY(dots_size=10, stroke=False, explicit_size=True, width=500, height=500)

  point_map = graphs.generate_point_map(7)
  edges = graphs.no_interesctions(point_map)

  xy_points = [(point.x, point.y) for point in point_map.values()]

  chart.add('Nodes', xy_points)
  for edge in edges:
    x, y = graphs.edge_to_pair(edge, point_map)
    chart.add('e', [(x.x, x.y), (y.x, y.y)], stroke=True, show_dots=False)

  return chart.render_response()

if __name__ == "__main__":
    app.run(debug=True)
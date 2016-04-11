from flask import Flask, render_template
import pygal
from pygal.style import NeonStyle
import random
import math
import graphs
from constraints import Node, Graph, backtrack
from pyrsistent import s

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("hello.html.j2")

@app.route("/chart.svg")
def chart():
    chart = pygal.XY(dots_size=10,
                     stroke=False,
                     explicit_size=True,
                     width=500,
                     height=500,
                     show_legend=False)

    point_map = graphs.generate_point_map(7)
    edges = graphs.no_interesctions(point_map)

    domain = s('red', 'green', 'blue')
    nodes = [Node(id=ix, point=y, color=None, domain=domain) for ix, y in point_map.items()]
    problem = Graph(edges=edges, nodes=nodes)

    try:
        solution = backtrack(nodes, problem)
        for node in solution:
            chart.add('node', [{'value':(node.point.x, node.point.y), 'color':node.color, 'label':str(node.id)}])
    except:
        print("oh nos!")
        for point in point_map.values():
            chart.add('node', [{'value':(point.x, point.y), 'color':'gray'}])

    #chart.add('Nodes', xy_points)
    for edge in edges:
        x, y = graphs.edge_to_pair(edge, point_map)
        chart.add('e', [(x.x, x.y), (y.x, y.y)], stroke=True, show_dots=False)

    return chart.render_response()

if __name__ == "__main__":
        app.run(debug=True)
from flask import Flask, render_template, request
import pygal
from pygal.style import NeonStyle
import random
import math
import graphs
from constraints import Node, Graph, BacktrackSolver
from pyrsistent import s
import uuid

app = Flask(__name__)

solutions = dict()

@app.route("/color_me_mine")
def hello():

    number_nodes = int(request.args.get('nodes', 6))

    identity = uuid.uuid1().hex
    point_map = graphs.generate_point_map(number_nodes)
    edges = graphs.no_interesctions(point_map)
    domain = s('red', 'green', 'blue', 'purple')
    nodes = [Node(id=ix, point=y, color=None, domain=domain) for ix, y in point_map.items()]

    problem = Graph(edges=edges, nodes=dict([(node.id, node) for node in nodes]))
    solver = BacktrackSolver()
    solution = solver.external_backtrack(problem)

    solutions[identity] = solution
    return render_template("hello.html.j2",
                           identity=identity,
                           runtime=solver.runtime,
                           backtrack_calls=solver.backtrack_calls,
                           constraint_tests=solver.constraint_tests,
                           failed_node_choice=solver.failed_node_choice)

@app.route("/chart")
def chart():
    identity = request.args.get('identity')

    chart = pygal.XY(dots_size=10,
                     stroke=False,
                     explicit_size=True,
                     width=500,
                     height=500,
                     show_legend=False)

    solution = solutions[identity]

    for node in solution.nodes.values():
        if node.color:
            color = node.color
        else:
            color = 'gray'

        chart.add('node', [{'value':(node.point.x, node.point.y), 'color':color, 'label':str(node.id)}])

    for edge in solution.edges:
        point_map = dict([(y.id, y.point) for y in solution.nodes.values()])
        x, y = graphs.edge_to_pair(edge, point_map)
        chart.add('e', [(x.x, x.y), (y.x, y.y)], stroke=True, show_dots=False, color='black')

    return chart.render_response()

if __name__ == "__main__":
        app.run(debug=True)
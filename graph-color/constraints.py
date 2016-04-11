"""
Backtracking for constraint satisfication

specifically, we wish to implement:

min-conflicts,
backtracking,
backtracking with forward checking,
and backtracking with MAC.

key questions:
how do we represent a CSP problem? (what does a Class CSP() look like)
what type of 'inference algorithm' do we use?
"""

import graphs
from pyrsistent import PClass, field, s
import random

class Graph(PClass):
    edges = field()
    nodes = field()

    def get_constraint_func(self, id):
        relevant_edges = [edge for edge in self.edges
                          if id in edge]

        nodes_to_compare = [ix for y in relevant_edges for ix in y.discard(id)]
        compare_colors = [(self.nodes[ix].id, self.nodes[ix].color) for ix in nodes_to_compare]

        def valid_assignment(color):
            return all([color != x[1] for x in compare_colors if x])

        return valid_assignment

def backtrack(nodes, problem):
    if all([y.color for y in nodes]):
        # all nodes have an assignment
        return nodes

    node_view = random.choice([y for y in nodes if not y.color])
    remaining_domain = node_view.domain

    constraints = problem.get_constraint_func(node_view.id)

    for val in remaining_domain:
        if constraints(val):
            # put val in the color
            new_node = node_view.set(color=val)
            new_nodes = [node for node in nodes if node.id != new_node.id] + [new_node]
            new_problem = problem.set(nodes=dict([(node.id, node) for node in new_nodes]))
            status = backtrack(new_nodes, new_problem)
            if status:
                return status
        else:
            print("failed constraint", val)
    print("failed all constraints", remaining_domain)

class Node(PClass):
    id = field(int)
    point = field(type=graphs.Point)
    color = field()
    domain = field()

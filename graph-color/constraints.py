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
import time

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

class BacktrackSolver():
    def __init__(self):
        self.start_time = 0
        self.stop_time = 0
        self.backtrack_calls = 0
        self.constraint_tests = 0
        self.failed_node_choice = 0

    def external_backtrack(self, problem):
        self.start_time = time.time()
        soln = self.backtrack(problem)
        self.stop_time = time.time()
        self.runtime = self.stop_time - self.start_time
        return soln

    def backtrack(self, problem):
        self.backtrack_calls += 1
        if all([y.color for y in problem.nodes.values()]):
            # all nodes have an assignment
            return problem

        node_view = random.choice([y for y in problem.nodes.values() if not y.color])
        remaining_domain = node_view.domain

        constraints = problem.get_constraint_func(node_view.id)

        for val in remaining_domain:
            if constraints(val):
                self.constraint_tests += 1
                # put val in the color
                new_node = node_view.set(color=val)
                new_nodes = [node for node in problem.nodes.values() if node.id != new_node.id] + [new_node]
                new_problem = problem.set(nodes=dict([(node.id, node) for node in new_nodes]))
                status = self.backtrack(new_problem)
                if status:
                    return status
        self.failed_node_choice += 1

class Node(PClass):
    id = field(int)
    point = field(type=graphs.Point)
    color = field()
    domain = field()

import unittest
import graphs
from graphs import Point
from pyrsistent import s, pset

class GraphTests(unittest.TestCase):
  def setUp(self):
    self.test_points = {0: Point(x=0.1, y=0.1),
              1: Point(x=0.9, y=0.95),
              2: Point(x=0.15, y=0.9),
              3: Point(x=0.95, y=0.1),
              4: Point(x=0.55, y=0.55)}

  def test_add_edges(self):
    edges = graphs.add_edges(self.test_points)
    self.assertTrue(len(edges) == 4)

  def test_point(self):
    pnt = graphs.Point(x=0.5, y=0.5)
    sol = graphs.Point(x=-0.5, y=-0.5)

    diff = pnt.diff(graphs.Point(x=1.0, y=1.0))
    self.assertEqual(sol, diff)

  def test_affine_intersect(self):
    pair_a = (Point(x=1., y=1.), Point(x=4., y=4.))
    pair_b = (Point(x=1., y=4.), Point(x=4., y=1.))

    self.assertTrue(graphs.find_affine_intersection(pair_a, pair_b))

  def test_affine_intersect(self):
    pair_a = (Point(x=1., y=1.), Point(x=1., y=4.))
    pair_b = (Point(x=4., y=4.), Point(x=4.1, y=1.))

    self.assertFalse(graphs.find_affine_intersection(pair_a, pair_b))

  def test_affine_intersect(self):
    pair_a = (Point(x=1., y=1.), Point(x=1., y=4.))
    pair_b = (Point(x=4., y=4.), Point(x=4., y=1.))

    self.assertFalse(graphs.find_affine_intersection(pair_a, pair_b))

  def test_affine_intersect(self):
    pair_a = (Point(x=4., y=4.), Point(x=1., y=1.))
    pair_b = (Point(x=1., y=4.), Point(x=4., y=1.))

    self.assertTrue(graphs.find_affine_intersection(pair_a, pair_b))

  def test_more_edges(self):
    edg = graphs.no_interesctions(self.test_points)
    self.assertEqual(pset(edg), s(s(1, 4), s(2, 4), s(3, 4), s(0, 4), s(1, 2), s(0, 2), s(0, 3), s(1, 3)))

  def test_an_edge(self):
    pair_a = graphs.edge_to_pair(s(0, 1), self.test_points)
    pair_b = graphs.edge_to_pair(s(4, 3), self.test_points)
    self.assertFalse(graphs.find_affine_intersection(pair_a, pair_b))

  def test_another_edge(self):
    pair_a = graphs.edge_to_pair(s(2, 4), self.test_points)
    pair_b = graphs.edge_to_pair(s(4, 1), self.test_points)
    self.assertFalse(graphs.find_affine_intersection(pair_a, pair_b))


if __name__ == '__main__':
  unittest.main()
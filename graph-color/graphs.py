import random
import math
from pyrsistent import s, pset, PClass, field, plist

def random_k(k):
    """Generates a list of k random numbers"""
    return [random.random() for y in range(k)]

def generate_point_map(k):
    """Generates and indexed set of k points"""
    xy_points = [Point(x=y[0], y=y[1])
                 for y in zip(random_k(k), random_k(k))]
    point_map = dict(enumerate(xy_points))
    return point_map

def add_edges(point_map):
    """Simple edge creation that adds edges only between a point and its nearest
    neighbor"""
    edges = []
    for anchor in point_map.keys():
        distances = [(search, distance(point_map[anchor], point_map[search]))
                     for search in set(point_map.keys()).difference({anchor})]

        min_distance = min(distances, key=lambda y: y[1])
        edges.append(s(anchor, min_distance[0]))
    return pset(edges)

def no_interesctions(point_map):
    """Finds all of the graph edges such that all nodes are connected and no
    edges 'intersect' on the 2d plane"""
    all_edges = pset([s(anchor, search)
                      for anchor in point_map.keys()
                      for search in point_map.keys()
                      if anchor != search])
    edges_by_distance = sorted(plist(all_edges), key=lambda y: edge_distance(y, point_map))

    edges = []
    for edge in edges_by_distance:
        pair_a = edge_to_pair(edge, point_map)
        if not any([find_affine_intersection(pair_a, edge_to_pair(y, point_map)) for y in edges]):
            edges.append(edge)

    return edges

def edge_distance(edge, point_map):
    """Returns the distance between two points in an edge"""
    a, b = edge_to_pair(edge, point_map)
    return distance(a, b)

def edge_to_pair(edge, point_map):
    """Returns the pair of points in an edge"""
    indexable = plist(edge)
    return (point_map[indexable[0]], point_map[indexable[1]])

def find_affine_intersection(pair_a, pair_b):
    """ Solve by finding the solution of a + lmb(a'-a) = b + eta(b'-b)
    where a is pair_a and b is pair_b. If lmb and eta are both in (0,1) then there
    is an intersection within the segments"""

    a, b = pair_a
    x, y = pair_b
    if (a == x) or (a == y) or (b == x) or (b == y):
        # if we are evaluating a corner case, then we should return immediately,
        # other wise we may error of floating-point ops.
        return False

    a_prime = b.diff(a)
    x_prime = y.diff(x)
    r = x.diff(a)

    # do some maths!
    try:
        eta = (r.x - r.y*a_prime.x/a_prime.y)/((a_prime.x*x_prime.y)/a_prime.y  - x_prime.x)
        lmb = (r.y + x_prime.y*eta)/a_prime.y
    except ZeroDivisionError:
        return False

    return (eta > 0) and (eta < 1) and (lmb > 0) and (lmb < 1)

class Point(PClass):
    x = field(float)
    y = field(float)
    def diff(self, point):
        return Point(x=self.x - point.x, y=self.y-point.y)

def distance(point_a, point_b):
    """Returns the l2 distance between two Points"""
    return math.sqrt((point_a.x - point_b.x)**2 + (point_a.y - point_b.y)**2)

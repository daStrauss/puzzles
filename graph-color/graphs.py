import random
import math

def random_k(k):
  return [random.random() for y in range(k)]

def generate_point_map(k):
  xy_points = [y for y in zip(random_k(k), random_k(k))]
  point_map = dict(enumerate(xy_points))
  return point_map

def add_edges(points):
  edges = []
  for anchor in point_map.keys():
    distances = [(search, distance(point_map[anchor], point_map[search]))
     for search in set(point_map.keys()).difference({anchor})]

    min_distance = min(distance, key=lambda y: y[1])
    edges.append({anchor, min_distance[0]})
  return point_map, edges

def distance(point_a, point_b):
  return math.sqrt((point_a[0] - point_b[0])**2 + (point_a[1] - point_b[1])**2)
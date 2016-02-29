package graph

trait Solver[S, A] {
  def solve(initialPuzzle: S): Node[S, A]
  def expandSolution(solution: Node[S, A]): List[(A, S)]
}

trait Node[S, A] {
  def state: S
  def pathCost: Int
}

case class Leaf[S, A](
  state: S,
  parent: Node[S, A],
  action: A,
  pathCost: Int
) extends Node[S, A]

case class Root[S, A](
  state: S,
  pathCost: Int = 0
) extends Node[S, A]

package graph

import com.twitter.util.Future

import scala.annotation.tailrec

trait Solver[S, A] {
  def solve(initialPuzzle: S): Future[Node[S, A]]
  def expandSolution(solution: Node[S, A]): Future[List[(A, S)]] = {
    @tailrec
    def expand(node: Node[S, A], queue: List[(A, S)]): List[(A, S)] = node match {
      case leaf: Leaf[S, A] => expand(leaf.parent, queue :+ (leaf.action, leaf.state))
      case root: Root[S, A] => queue
    }
    Future {
      expand(solution, List.empty)
    }
  }
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

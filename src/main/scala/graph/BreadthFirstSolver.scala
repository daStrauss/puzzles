package graph

import scala.annotation.tailrec

trait BreadthFirstSolver[S, A] extends Solver[S, A] {
  def goalState: S
  type InternalNode = Node[S, A]
  def findChildren(state: S): List[(A, S)]

  @tailrec
  private[this] def search(exploredSet: Set[S], frontier: List[InternalNode]): InternalNode = {
    frontier match {
      case Nil => throw new RuntimeException("No Solutions Found")
      case head :: tail => {
        if (head.state == goalState) {
          head
        } else {
          val nextExplore = exploredSet + head.state
          val newChildren = findChildren(head.state).filterNot {
            case (action, state) => exploredSet.contains(state)
          }.filterNot {
            case (action, state) => frontier.map(_.state).contains(state)
          }.map {
            case (action, state) => Leaf(
              state = state,
              parent = head,
              action = action,
              pathCost = head.pathCost + 1
            )
          }
          val nextFrontier = tail ++ newChildren
          search(nextExplore, nextFrontier)
        }
      }
    }
  }

  def solve(puzzle: S): InternalNode = {
    val rootNode = Root[S, A](puzzle)
    val initialFrontier = findChildren(puzzle).map {
      case (action, child) => Leaf(
        state = child,
        parent = rootNode,
        action = action,
        pathCost = rootNode.pathCost + 1
      )
    }
    search(Set.empty, initialFrontier)
  }
}
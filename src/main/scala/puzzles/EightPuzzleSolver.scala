package puzzles

import graph.{Root, Leaf, Solver}

import scala.annotation.tailrec


class EightPuzzleSolver(
  goal: EightPuzzle
) extends Solver[EightPuzzle, Action]{

  @tailrec
  private[this] def search(exploredSet: Set[EightPuzzle], frontier: List[EightNode]): EightNode = {
    frontier match {
      case Nil => throw new RuntimeException("No solutions found")
      case head :: tail => {
        if (head.state == goal) {
          //winner winner chicken dinner
          head
        } else {
          val nextExplore = exploredSet + head.state
          val newChildren = EightPuzzleStateMachine.findChildren(head.state).filterNot {
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

  def solve(eightPuzzle: EightPuzzle): EightNode = {
    val rootNode = Root[EightPuzzle, Action](eightPuzzle)
    val initialFrontier = EightPuzzleStateMachine.findChildren(eightPuzzle).map {
      case (action, child) => Leaf(
        state = child,
        parent = rootNode,
        action = action,
        pathCost = rootNode.pathCost + 1
      )
    }
    search(Set.empty, initialFrontier)
  }

  def expandSolution(node: EightNode): List[(Action, EightPuzzle)] = {
    @tailrec
    def expand(node: EightNode, queue: List[(Action, EightPuzzle)]): List[(Action, EightPuzzle)] = node match {
      case leaf: Leaf[EightPuzzle, Action] => expand(leaf.parent, queue :+ (leaf.action, leaf.state))
      case root: Root[EightPuzzle, Action] => queue
    }
    expand(node, List.empty)
  }
}

object EightPuzzleSolver {
  val goal = EightPuzzle(A(), B(), C(), D(), E(), F(), G(), H(), X())
}

import scala.annotation.tailrec

object EightPuzzleSolver {
  val goal = EightPuzzle(A(), B(), C(), D(), E(), F(), G(), H(), X())

  @tailrec
  def search(exploredSet: Set[EightPuzzle], frontier: List[Node]): Node = {
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

  def solve(eightPuzzle: EightPuzzle): Node = {
    val rootNode = Root(eightPuzzle)
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

  def expandSolution(node: Node): List[(Action, EightPuzzle)] = {
    @tailrec
    def expand(node: Node, queue: List[(Action, EightPuzzle)]): List[(Action, EightPuzzle)] = node match {
      case leaf: Leaf => expand(leaf.parent, queue :+ (leaf.action, leaf.state))
      case root: Root => queue
    }
    expand(node, List.empty)
  }
}

trait Node {
  def state: EightPuzzle
  def pathCost: Int
}

case class Leaf(
  state: EightPuzzle,
  parent: Node,
  action: Action,
  pathCost: Int
) extends Node

case class Root(
  state: EightPuzzle,
  pathCost: Int = 0
) extends Node
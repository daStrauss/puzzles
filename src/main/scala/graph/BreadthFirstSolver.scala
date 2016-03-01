package graph

import com.twitter.util.Future

import scala.annotation.tailrec
import scala.collection.immutable.Queue

trait BreadthFirstSolver[S, A] extends Solver[S, A] {
  def goalState: S

  type InternalNode = Node[S, A]

  def findChildren(state: S): List[(A, S)]

  @tailrec
  private[this] def search(exploredSet: Set[S], frontier: Queue[InternalNode]): InternalNode = {
    if (frontier.isEmpty) {
      throw new RuntimeException("No Solutions Found")
    } else {
      val (head, tail) = frontier.dequeue
      if (head.state == goalState) {
        head
      } else if (exploredSet.contains(head.state)) {
        search(exploredSet, tail)
      } else {
        val nextExplore = exploredSet + head.state
        val newChildren = findChildren(head.state).filterNot {
          case (action, state) => exploredSet.contains(state)
        }.map {
          case (action, state) => Leaf(
            state = state,
            parent = head,
            action = action,
            pathCost = head.pathCost + 1
          )
        }
        val nextFrontier = tail.enqueue(newChildren)
        search(nextExplore, nextFrontier)
      }
    }
  }

  def solve(puzzle: S): Future[InternalNode] = {
    val rootNode = Root[S, A](puzzle)
    val initialFrontier = findChildren(puzzle).map {
      case (action, child) => Leaf(
        state = child,
        parent = rootNode,
        action = action,
        pathCost = rootNode.pathCost + 1
      )
    }.foldLeft(Queue.empty[Leaf[S,A]]){
      case (queue, leaf) => queue.enqueue(leaf)
    }
    Future {
      search(Set.empty, initialFrontier)
    }
  }
}
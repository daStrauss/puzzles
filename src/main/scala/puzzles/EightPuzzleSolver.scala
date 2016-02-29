package puzzles

import graph.BreadthFirstSolver

class EightPuzzleSolver(
  goal: EightPuzzle
) extends BreadthFirstSolver[EightPuzzle, Action] {
  val goalState = goal
  def findChildren(state: EightPuzzle) = EightPuzzleStateMachine.findChildren(state)
}

object EightPuzzleSolver {
  val goal = EightPuzzle(A(), B(), C(), D(), E(), F(), G(), H(), X())
}

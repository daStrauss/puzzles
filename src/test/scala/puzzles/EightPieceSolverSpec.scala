package puzzles

import org.scalatest.{Matchers, WordSpec}

class EightPieceSolverSpec extends WordSpec with Matchers {
  val testSolver = new EightPuzzleSolver(EightPuzzleSolver.goal)

  "Solving a simple puzzle" when {
    "using a simple puzzle" should {
      "use the right number of steps" in {
        val fiveDeep = List(MoveLeft(), MoveUp(), MoveRight(), MoveUp(), MoveLeft(), MoveDown())
          .foldLeft(EightPuzzleSolver.goal){
            case (state, action) => EightPuzzleStateMachine.update(action, state).get()
          }
        val sol = testSolver.solve(fiveDeep)
        sol.pathCost should be(6)
      }
    }
  }
}

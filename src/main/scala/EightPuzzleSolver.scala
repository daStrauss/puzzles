import com.twitter.util.Try

object EightPuzzleSolver {
  val goal = EightPuzzle(A(), B(), C(), D(), E(), F(), G(), H(), X())

}


object EightPuzzleStateMachine {
  def update(action: Action, state: EightPuzzle): Try[EightPuzzle] = {
    val xLocation = state.emptyLocation
    val swapLocation = action match {
      case MoveUp()    => (xLocation._1 - 1, xLocation._2)
      case MoveDown()  => (xLocation._1 + 1, xLocation._2)
      case MoveLeft()  => (xLocation._1, xLocation._2 - 1)
      case MoveRight() => (xLocation._1, xLocation._2 + 1)
    }
    state.switch(xLocation, swapLocation).filter(_ != state)
  }

  def children(state: EightPuzzle): List[EightPuzzle] =
    List(MoveUp(), MoveDown(), MoveLeft(), MoveRight()).flatMap(update(_, state).toOption)
}

sealed trait Action
case class MoveUp() extends Action
case class MoveDown() extends Action
case class MoveLeft() extends Action
case class MoveRight() extends Action


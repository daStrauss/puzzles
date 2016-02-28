import org.scalatest.{Matchers, WordSpec}

class EightPuzzleStateMachineSpec extends WordSpec with Matchers {
  "An Eight Puzzle State Machine" when {
    "Advancing states" should {
      "find all children" in {
        val initial = EightPuzzle(B(), C(), A(), D(), E(), X(), F(), G(), H())
        val children = EightPuzzleStateMachine.findChildren(initial)

        val knownChildren = Set(
          EightPuzzle(B(), C(), X(), D(), E(), A(), F(), G(), H()),
          EightPuzzle(B(), C(), A(), D(), X(), E(), F(), G(), H()),
          EightPuzzle(B(), C(), A(), D(), E(), H(), F(), G(), X())
        )
        children.map(_._2).toSet should be(knownChildren)
      }
    }
  }
}

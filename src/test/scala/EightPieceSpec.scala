import com.twitter.util.Try
import org.scalatest.{Matchers, WordSpec}

class EightPieceSpec extends WordSpec with Matchers {
  "EightPiece" when {
    "Constructing" should {
      "resucitate itself" in {
        val parsed = EightPuzzle.fromRowFlat("ABCDEFGHX").toOption
        parsed should be(Some(EightPuzzle(A(), B(), C(), D(), E(), F(), G(), H(), X())))
      }
    }
    "accessing and finding" should {
      "find the upper corner" in {
        EightPuzzleSolver.goal.get(0,0) should be(A())
      }
      "find the middle" in {
        EightPuzzleSolver.goal.get(1,1) should be(E())
      }
      "find the lower left" in {
        EightPuzzleSolver.goal.get(2, 0) should be(G())
      }
      "find the right X" in {
        EightPuzzleSolver.goal.emptyLocation should be((2,2))
      }
    }
    "swapping" should {
      "create a real result" in {
        val result = EightPuzzleSolver.goal.switch((0,0), (1,1)).toOption
        result should be(Some(EightPuzzle(E(), B(), C(), D(), A(), F(), G(), H(), X())))
      }
      "take no action on the edge" in {
        val result = EightPuzzleSolver.goal.switch((0,0), (-1, -1)).toOption
        result should be(Some(EightPuzzleSolver.goal))
      }
    }
  }
}

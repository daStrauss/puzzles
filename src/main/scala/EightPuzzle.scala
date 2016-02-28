import com.twitter.util.Try

import scala.annotation.tailrec
import scala.util.Random

case class EightPuzzle(
  loc11: Piece,
  loc12: Piece,
  loc13: Piece,
  loc21: Piece,
  loc22: Piece,
  loc23: Piece,
  loc31: Piece,
  loc32: Piece,
  loc33: Piece
) {
  private val listForm = List(loc11, loc12, loc13, loc21, loc22, loc23, loc31, loc32, loc33)
  def get(row: Int, col: Int): Piece =
    listForm(positionToIndex(row, col))

  def switch(locA: (Int, Int), locB: (Int, Int)): Try[EightPuzzle] = {
    val atA = listForm(posToI(locA))
    val atB = listForm(posToI(locB))

    val newList = listForm.updated(posToI(locB), atA).updated(posToI(locA), atB)
    Try(newList).map {
      case l1 :: l2 :: l3 :: l4 :: l5 :: l6 :: l7 :: l8 :: l9 :: Nil =>
        EightPuzzle(l1, l2, l3, l4, l5, l6, l7, l8, l9)
    }
  }

  private def posToI(loc: Tuple2[Int, Int]) = {
    positionToIndex(loc._1, loc._2)
  }

  private def positionToIndex(row: Int, col: Int) = {
    row.min(2).max(0)*3 + col.min(2).max(0)
  }

  private def indexToPosition(pos: Int) = (pos/3, pos % 3)

  def emptyLocation = indexToPosition(listForm.zipWithIndex.find(_._1 == X()).head._2)

  def prettyPrint: Unit = println(listForm.sliding(3,3).toList.map(_.mkString("\t")).mkString("\n"))
}

object EightPuzzle {
  def fromRowFlat(input: String): Try[EightPuzzle] = {
    Try.collect(input.map(Piece.fromString).toList).map {
      case l1 :: l2 :: l3 :: l4 :: l5 :: l6 :: l7 :: l8 :: l9 :: Nil =>
        EightPuzzle(l1, l2, l3, l4, l5, l6, l7, l8, l9)
    }
  }

  def random(): EightPuzzle = {
    val places: List[Piece] = List(A(), B(), C(), D(), E(), F(), G(), H(), X())

    scala.util.Random.shuffle(places) match {
      case l1 :: l2 :: l3 :: l4 :: l5:: l6 :: l7 :: l8 :: l9 ::Nil =>
        EightPuzzle(l1, l2, l3, l4, l5, l6, l7, l8, l9)
      case _ => throw new RuntimeException("something weird happened")
    }
  }

  def random(steps: Int) = {
    @tailrec
    def step(level: Int, state: EightPuzzle): EightPuzzle = {
      if (level == 0) {
        state
      } else {
        val nsz = Random.shuffle(EightPuzzleStateMachine.findChildren(state))
        step(level - 1, nsz.map(_._2).head)
      }
    }
    step(steps, EightPuzzleSolver.goal)
  }
}


sealed trait Piece {
  override def toString = this.getClass().getName()
}
case class A() extends Piece
case class B() extends Piece
case class C() extends Piece
case class D() extends Piece
case class E() extends Piece
case class F() extends Piece
case class G() extends Piece
case class H() extends Piece
case class X() extends Piece


object Piece {
  def fromString(input: Char): Try[Piece] = Try {
    input match {
      case 'A' => A()
      case 'B' => B()
      case 'C' => C()
      case 'D' => D()
      case 'E' => E()
      case 'F' => F()
      case 'G' => G()
      case 'H' => H()
      case 'X' => X()
    }
  }
}
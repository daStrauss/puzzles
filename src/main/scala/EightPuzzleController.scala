import com.twitter.finagle.http.Request
import com.twitter.finatra.http.Controller
import com.twitter.finatra.request.QueryParam

class EightPuzzleController extends Controller {
  get("/") { request: Request =>
    response.ok.view("hello.mustache", Map("title"->""))
  }

  get("/new_puzzle") { request: Request =>
    val simplePuzzle = EightPuzzle.random(20)
    response.ok.view(
     "puzzle_view.mustache",
     puzzleViewData("new puzzle", simplePuzzle)
    )
  }
  get("/up/:puzzle") { request: PuzzleRequest =>
    EightPuzzle.fromRowFlat(request.puzzle)
      .flatMap(EightPuzzleStateMachine.update(MoveUp(),_)).map { puzzle =>
      response.ok.view(
        "puzzle_view.mustache",
        puzzleViewData("went up", puzzle)
      )
    }.toOption
  }

  get("/down/:puzzle") { request: PuzzleRequest =>
    EightPuzzle.fromRowFlat(request.puzzle)
      .flatMap(EightPuzzleStateMachine.update(MoveDown(),_)).map { puzzle =>
      response.ok.view(
        "puzzle_view.mustache",
        puzzleViewData("went Down", puzzle)
      )
    }.toOption
  }

  get("/left/:puzzle") { request: PuzzleRequest =>
    EightPuzzle.fromRowFlat(request.puzzle)
      .flatMap(EightPuzzleStateMachine.update(MoveLeft(),_)).map { puzzle =>
      response.ok.view(
        "puzzle_view.mustache",
        puzzleViewData("went left", puzzle)
      )
    }.toOption
  }

  get("/right/:puzzle") { request: PuzzleRequest =>
    EightPuzzle.fromRowFlat(request.puzzle)
      .flatMap(EightPuzzleStateMachine.update(MoveRight(),_)).map { puzzle =>
      response.ok.view(
        "puzzle_view.mustache",
        puzzleViewData("went right", puzzle)
      )
    }.toOption
  }

  get("/show_solution/:puzzle") { request: PuzzleRequest =>
    EightPuzzle.fromRowFlat(request.puzzle)
      .map { puzzle =>
        val solution = EightPuzzleSolver.solve(puzzle)
        val path = EightPuzzleSolver.expandSolution(solution)
        val actions = path.map(_._1.getClass.getName).reverse.mkString(" -> ")
        val puzzleView = puzzleViewData("Solution", puzzle) ++ Map("solution"->true, "actions" -> actions)
        response.ok.view(
          "puzzle_view.mustache",
          puzzleView
        )
      }.toOption
  }

  private[this] def puzzleViewData(title: String, puzzle: EightPuzzle): Map[String, Any] = {
    val moves = EightPuzzleStateMachine.findChildren(puzzle).map(_._1)
      .map(_.getClass.getName)
      .map((_, true))
      .toMap
    Map(
      "title" -> title,
      "puzzleString" -> puzzle.straightPrint,
      "loc11" -> puzzle.loc11.toString,
      "loc12" -> puzzle.loc12.toString,
      "loc13" -> puzzle.loc13.toString,
      "loc21" -> puzzle.loc21.toString,
      "loc22" -> puzzle.loc22.toString,
      "loc23" -> puzzle.loc23.toString,
      "loc31" -> puzzle.loc31.toString,
      "loc32" -> puzzle.loc32.toString,
      "loc33" -> puzzle.loc33.toString
    ) ++ moves
  }
}

case class UnsolvedPuzzle(
  title: String,
  puzzleString: String,
  loc11: String,
  loc12: String,
  loc13: String,
  loc21: String,
  loc22: String,
  loc23: String,
  loc31: String,
  loc32: String,
  loc33: String,
  moves: Map[String, String]
)

case class PuzzleRequest(
  @QueryParam puzzle: String
)
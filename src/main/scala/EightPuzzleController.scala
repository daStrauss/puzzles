import com.twitter.finagle.http.Request
import com.twitter.finatra.http.Controller

class EightPuzzleController extends Controller {
  get("/") { request: Request =>
    response.ok.body("Hello")
  }
}

import com.twitter.finatra.http.HttpServer
import com.twitter.finatra.http.filters.CommonFilters
import com.twitter.finatra.http.modules.MustacheModule
import com.twitter.finatra.http.routing.HttpRouter
import com.twitter.inject.TwitterModule

object PuzzleServerMain extends PuzzleServer

class PuzzleServer extends HttpServer {
  override def modules: Seq[TwitterModule] = Seq(
    MustacheModule
  )

  override def configureHttp(router: HttpRouter): Unit  = {
    router
      .filter[CommonFilters]
      .add[EightPuzzleController]
  }
}

import com.twitter.finatra.http.HttpServer
import com.twitter.finatra.http.filters.{CommonFilters, LoggingMDCFilter, TraceIdMDCFilter}
import com.twitter.finatra.http.routing.HttpRouter


object PuzzleServerMain extends PuzzleServer

class PuzzleServer extends HttpServer {
  override def configureHttp(router: HttpRouter): Unit  = {
    router
      .add[EightPuzzleController]
  }
}
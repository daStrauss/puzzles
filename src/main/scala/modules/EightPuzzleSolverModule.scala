package modules

import com.google.inject.{Provides, Singleton}
import com.twitter.inject.TwitterModule
import puzzles.EightPuzzleSolver

object EightPuzzleSolverModule extends TwitterModule {
  @Singleton
  @Provides
  def providesEightPuzzleSolver: EightPuzzleSolver = {
    new EightPuzzleSolver(EightPuzzleSolver.goal)
  }
}

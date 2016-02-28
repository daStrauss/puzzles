
import sbt.Keys._
//import sbtassembly.{PathList, MergeStrategy}
//import spray.revolver.RevolverPlugin._

lazy val versions = new {
  val finatra       = "2.1.4"
}
lazy val commonSettings = Seq(
  organization := "dave",
  scalaVersion := "2.11.7",
  libraryDependencies ++= Seq(
    "org.slf4j" % "slf4j-simple" % "1.7.10",
    "com.twitter.finatra" % "finatra-http_2.11" % versions.finatra,
    "com.twitter.finatra" % "finatra-slf4j_2.11" % versions.finatra,
    "com.twitter.finatra" %% "finatra-httpclient" % versions.finatra,
    "com.twitter.inject" %% "inject-core" % versions.finatra,
    "org.scalatest" %% "scalatest" % "2.2.6"
  )
)

lazy val root = (project in file(".")) settings(commonSettings: _*)



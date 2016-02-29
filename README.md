## A Simple Finatra App
I wanted to do a proof of concept app for finatra _and_ think about graph search algorithms. So here's a little puzzle solver.

Currently only breadth-first search is built which is tiresomely slow if the problems get really jumbled.

To get this running locally:

1. check it out from github
2. start sbt: `sbt`
3. run revolver: `re-start`
4. Point your browser to `localhost:8888` unless you changed the default port.
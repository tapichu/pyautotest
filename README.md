# pyAutotest

The aim of this project is to simplify TDD by running tests continuously.

## Unit test libraries

pyAutotest should be relatively generic so it is simple to add support for different unit test libraries like _unittest_, _doctest_, etc.

I'll start with _maven_ because I'm using it at work and it can be painful testing with it.

## Inspiration

My co-workers' frustration with _maven_.

David Beazley's [Generator Tricks for System Programmers](http://www.dabeaz.com/generators/) gave me the idea of using python's generators to build a processing pipeline. It should be easy to have a _common_ pipeline and just plug-in a couple of stages with the specifics of a certain unit test library.


[CS5Lab]: https://www.cs.hmc.edu/twiki/bin/view/CS5/SoundsGoodLab
[Frequencies]: http://en.wikipedia.org/wiki/Piano_key_frequencies

# Fluency lab

Many DSLs start as libraries or APIs and, over time, grow into full-fledged
languages. A first-draft library is a low-cost way to experiment with language
design. In this lab, we'll do a first-draft design of a sound-processing 
library. The goal is to get practice writing a *fluent* library, that
is: a library that makes it easier and more natural for its users to accomplish
specific tasks.

## The lab
This lab revisits one that was created for CS 5. In CS 5, the goal is to learn
about Python's functional programming capabilities, including:

   + [lists](http://www.tutorialspoint.com/python/python_lists.htm)
   + [list comprehensions](https://docs.python.org/2/tutorial/datastructures.html#list-comprehensions)
   + [`map`, `filter`, `reduce`](http://www.python-course.eu/lambda.php)
   + function definitions and calls

In contrast, we will *use* those features to design an easy-to-use library. 

## Getting started
   1. Fork this repository, which contains all the Python and sound files you'll
   need.
   1. Submit a pull request right away. (The pull request will be updated as
   you work on the lab.)
   1. Head over to the CS 5 writeup. Take a brief look at the top of the file,
   to see a description of the files. Then, skim / skip down to the section
   titled "Sound coding...". Start doing the lab from there. (The earlier part
   of the lab, which creates some helper function has already been completed in
   the `hw3pr1.py` file that comes with this repository.)

## Goals and constraints
Our goals are a bit different from the Python lab. If you follow the
instructions in the lab, you'll find that you create a library that's not as
easy to use as we'd like. You're goal is to improve on the design. 

In particular, focus on the following:

   + Make it easier for a user of the library to combine multiple sound effects
   in a single file
   
   + As much as possible, try to use a limited toolkit to create your library.
   In particular, reach first for the language features mentioned at the top of
   this lab. If those tools don't seem up for the job, then you can reach for
   other tools (e.g., `for` loops, classes, etc.).
   
   + As a stretch goal, see if you can make it easy for a library user to
   compose a song of arbitrary sounds. This 
   [information about sound frequencies][Frequencies] may help. If you're
   looking for a test song, here are the notes for *Twinkle, twinkle, little
   star*:

          A A E E F# F# E
          D D C# C# B B A
          E E D D C# C# B
          E E D D C# C# B
          A A E E F# F# E
          D D C# C# B B A


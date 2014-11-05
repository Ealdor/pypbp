pypbp
=====
Python Paint by Pairs: an implementation of the nonogram **Paint by Pairs** using pygame and python 2.7.8.

###Rules:
**Link-a-Pix** (also known as "Paint by Pairs") consists of a grid, with numbers filling some squares; pairs of numbers must be located correctly and connected with a line filling a total of squares equal to that number. Squares containing '1' represent paths that are 1-square long. Paths may follow any horizontal or vertical direction. Paths are not allowed to cross other paths.

There is only one unique way to link all the squares in a properly-constructed puzzle. When completed, the squares that have lines are filled; the contrast with the blank squares reveals the picture.

###Keys:
* Use *key arrows* to move through the puzzle table. Use *x* while move to move faster.
* Use *space* while move to draw the lines.
* Use *c* to delete a line.
* Use *-* to zoom out and *+* to restore to original zoom. You cannot move or paint if there is zoom.

###Considerations:
Puzzles are inside puzzle directory. To launch the game write on a terminal: 
> python pypbp.py filename [PUZZLE_WIDTH] [PUZZLE_HEIGHT]

> python pypbp.py generator/puzzles/test_11x11.csv 11 11

* Inside the generator directory the is a generator scrypt (and a solver one) to generate new puzzles from image bitmap (CSV or JSON). See the examples.
* Puzzles can be from 1x1 to 800x800 (or so).
* Game resolution is set to: 1024x600

###Puzzle Generator and Solver:
The code and some examples were taken from: https://code.cs.nott.ac.uk/p/gp13-jaa/. So all credits for them.
To use the generator:
> python generator.py [PUZZLE_WIDTH] [PUZZLE_HEIGHT] [PUZZLE_NAME] [PUZZLE_DIFFICULTY (4-10)]

> python generator.py 10 10 gentestconv.json 5

This will generate a *temp.csv* or *temp.json* file with the generated puzzle.

###Contact:
ealdorj@gmail.com
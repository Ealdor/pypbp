pypbp
=====
Python Paint by Pair: an implementation of the nonogram **Paint by Pair** using pygame and python 2.7.8.

###Rules:
**Link-a-Pix** (also known as "Paint by Pairs") consists of a grid, with numbers filling some squares; pairs of numbers must be located correctly and connected with a line filling a total of squares equal to that number. Squares containing '1' represent paths that are 1-square long. Paths may follow any horizontal or vertical direction. Paths are not allowed to cross other paths.

There is only one unique way to link all the squares in a properly-constructed puzzle. When completed, the squares that have lines are filled; the contrast with the blank squares reveals the picture.

###Keys:
* Use *key arrows* to move through the puzzle table. Use *x* while move to move faster.
* Use *space* while move to draw the lines.
* Use *c* to delete a line.

###Considerations:
To launch the game write on a terminal: 
> python pypbp.py filename

See the file *test_11x11.txt* for an example of a puzzle. The program does not check if the puzzle is valid or not. Syntax: 
* First line: number of columns, number of rows
* Line: number of the cell


Puzzles can be from 1x1 to 800x800 (or so).
Game resolution is set to: 1024x600

###Contact: ealdorj@gmail.com

pypbp
=====
Python Paint by Pairs: an implementation of the nonogram **Paint by Pairs** using pygame and python 2.7.8.

###Rules:
**Link-a-Pix** (also known as "Paint by Pairs") consists of a grid, with numbers filling some squares; pairs of numbers must be located correctly and connected with a line filling a total of squares equal to that number. Squares containing '1' represent paths that are 1-square long. Paths may follow any horizontal or vertical direction. Paths are not allowed to cross other paths.

There is only one unique way to link all the squares in a properly-constructed puzzle. When completed, the squares that have lines are filled; the contrast with the blank squares reveals the picture.

###Keys:
* Use *key arrows* to move through the puzzle. Use *x* while move to scroll faster.
* Use *space* while move to draw the lines between two numbers.
* Use *c* to delete a line.
* Use *-* to zoom out and *+* to restore to original zoom. You cannot move or paint if there is a zoom active.

###Considerations:
Puzzles are inside puzzle directory. A puzzle can be CSV (b&w) or JSON (color). To launch the game write on a terminal: 

> python main.py <filename>

> python main.py puzzles/toad_50x50.csv

> python main.py mario_50x46.json

* Inside the generator directory there is a generator script to generate new puzzles from an image bitmap (CSV or JSON).
* Puzzles can be from 1x1 to 800x800 (or so).
* Game resolution is set to: 1024x600 (window is resizeable).

###Puzzle Generator:
To use the generator:
> python generator.py <file_path> <maxim> <iters> 

Where:
* maxim: max length number (1 - 21).
* iters: number of iterations per number. Higher number means more complexity but more time to generate the puzzle (a good value is 20 or so).

> python generator.py gentestconv_20x20.csv 21 10

This will generate a *temp.csv* or *temp.json* file with the generated puzzle.

###Utils:
Inside *Utils* directory there are two scripts to generate a puzzle (only 1's) from an image.

> python img_to_csv.py <image_name> <width> <height>

> python img_to_json.py <image_name> <width> <height>

This will generate a *csv* or *json* file. After this you can generate a complete puzzle with the Puzzle Generator.

###TODO:
* Make a gui to select the puzzle and configure the resolution/fullscreen.
* Mouse support.
* Update the generator to generate color puzzles.

###Contact:
ealdorj@gmail.com
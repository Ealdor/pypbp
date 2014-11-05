"""
	constants.py
	~~~~~~~~~

	This module contains the constants and settings that are
	used throughout the project.

	:Mandla Moyo, 2014.
"""

#Indices
X = 0
Y = 1
VALUE = 2
TYPE = 3
START_ID = 4
END_ID = 5
COLOUR = 6
PID = 4

EMPTY = 0
END = 1
PATH = 2

XSIZE = 1
YSIZE = 2
FILENAME = 3

FIRST = 0
SECOND = 1

#Tags
MINIMUM_NODECOUNT = 2
ANY_VALUE = -1
EMPTY_LIST = []
LIMIT = 4
MAX_LIMIT = 10
LIMIT_CONSTANT = 1.25
MAX_ATTEMPTS = 5

#Colours
BLACK = [0,0,0]
WHITE = [255,255,255]

#Error Flags
UNDERPOPULATION_ERROR = 1
NO_MATCH_ERROR = -1
MERGE_ERROR = -1

#File Settings
CSV = "csv"
JSON = "json"

PUZZLE_DIRECTORY = "puzzles/"

OUTPUT_FILENAME_GENERATOR = "temp"
OUTPUT_FILENAME_SOLVER = "tempsolved"

OUTPUT_FILETYPE_GENERATOR = JSON
OUTPUT_FILETYPE_SOLVER = JSON

INIT_VALUE = [0,0,0,EMPTY,0,0,WHITE]
UNKNOWN = ' '
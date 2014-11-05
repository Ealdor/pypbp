"""
	grid.py
	~~~~~~~~~

	This module describes the core interface for a basic Grid object.
	
	The grid is the main data structure used to manipulate cells in order both to generate and solve Link-a-Pix puzzles. The parent Grid class implements various utility, cell handling, and file handling operations, allowing generating and solving functionality to be separated into particular child classes.
	
	:Mandla Moyo, 2014.
"""

from pattern import getRotations, getRelativePos, getAbsolutePos, getRelativePath, getEuclidianDistance, addMirrors
from cellReader import Cell, CsvCellReader, JsonCellReader
from pathContainer import PathContainer 
from constants import *

class Grid( object ):
	""" The Grid class is used to contain and manipulate puzzle data as
	specified by particular Cell configurations.
	"""
	def __init__( self, x, y, limit=MAX_LIMIT ):
		self.grid = []
		self.cellList = []
		self.dimensions = [x,y]
		self.pathList = PathContainer()
		self.readers = { CSV: CsvCellReader( self.dimensions ), JSON: JsonCellReader( self.dimensions ) }
		self.limit = limit

	
	""" INITIALIZATION
	"""
	def build( self ):
		for j in range( self.dimensions[Y] ):
			cells = []
			for i in range( self.dimensions[X] ):
				cell = Cell( [i,j] )
				cells.append(cell)
				self.cellList.append(cell)
			self.grid.append( cells )
			
	

		
	""" UTILITY FUNCTIONS
	"""
	def isValidPos( self, pos ):
		for i in range(len(pos)):
			if( pos[i] < 0 or pos[i] >= self.dimensions[i] ): return False
			
		return True
	
	def isReachable( self, p1, p2 ):
		"""Returns True if p1 reachable from p2 and visa versa.
		"""
		res = abs( p1[0]-p2[0] ) + abs( p1[Y] - p2[Y] )
		v = self.getCellAt( p1 ).getValue()

		return res < v and res%2 != v%2
		
		
	""" CELL HANDLING FUNCTIONS
	"""
	def getCellAt( self, pos ):
		return self.grid[pos[Y]][pos[X]]
	
	def getCellList( self ):
		return self.cellList
		
	def setCellInfo( self, cellInfo ):
		pass
		
	def getCellInfo( self ):
		return [cell.getInfo() for cell in self.getCellList()]
	
	def getReachable( self, pos ):
		pass
		
	""" FILE I/O HANDLING
	"""
	def importGrid( self, name, fileType ):
		"""Reads in cell data from the specified file, and uses it to update Grid cells
				Read data format: [[xpos, ypos, value, type, startId, endId, colourCode],..]
		"""
		data = self.readers[fileType].readGrid( name )
		self.setCellInfo( data )
		
	def exportGrid( self, name, fileType ):
		"""Takes the current set of stored cells, and passes them to the specified reader
		to be written to a given file.
		"""
		self.readers[fileType].writeGrid( name, self.getCellList() ) #,True)
	
	

####################################
# testSolve.py



####################################
# pgen.py


"""
	solver.py (RENAME)
	~~~~~~~~~

	Solver for G52GRP Link-A-Pix Project
	
	This module implements the solving functionality for a given puzzle configuration.
	The program takes 3 arguments on the command line, and outputs the puzzle solution
	to a temp file (of name and type specified in constants.py) in the specified puzzle
	directory.
	
	Command line interface:
		$ python solver.py [PUZZLE_WIDTH] [PUZZLE_HEIGHT] [PUZZLE_NAME]
		(PUZZLE_NAME is a type-specified name of a file located in the directory specified in constants.py)
		
	:Mandla Moyo, 2014.
"""

from cellReader import Cell, CsvCellReader, JsonCellReader
from pathContainer import PathContainer
from math import pi, cos, sin
from random import randint, shuffle, choice
from grid import Grid
from pattern import getRotations, getRelativePos, getAbsolutePos, getRelativePath, getEuclidianDistance, addMirrors
from constants import *
from copy import deepcopy
import sys

GRID = 0
FREE = 1
CELLS = 2

class SolveGrid( Grid ):
	def __init__( self, x, y ):
		Grid.__init__( self, x, y )
		self.initEndCells = 0
		self.build()
		self.backTrackMap = {}
		
	def build( self ):
		for j in range( self.dimensions[Y] ):
			cells = []
			for i in range( self.dimensions[X] ):
				cell = Cell( [i,j] )
				cells.append(cell)
				self.cellList.append(cell)
			self.grid.append( cells )
	
	
	def setCellInfo( self, cellInfo ):
		"""Takes the information from a file reader, and uses it to set the values of 
		the grid's cells.
		"""
		for info in filter( lambda x: x[TYPE] == END, cellInfo ):
			cell = self.grid[ info[Y] ][ info[X] ]
			cell.setValue( info[VALUE] )
			cell.setType( info[TYPE] )
			cell.setPathIds( info[START_ID], info[END_ID] )
			cell.setColour( info[COLOUR] )
	

	def checkValid( self ):
		"""Returns false if the board configuration violates any basic principles of complete-ability.
			Tests to make sure:
				1) There is an even number of end cells (all cells can be paired),
				2) All cells are reachable from at least one other cell of equal value.
		"""
		
		endCells = self.getCellType( END )
		
		# Even number of endpoints?
		if len( endCells ) % 2 != 0: return False
		
		# All endpoints have other reachable endpoints of equal value?
		for cell in endCells:
			if len( getReachable( cell.pos )) == 0: return False
		
		return True
	

	def getReachable( self, pos ):
		"""Returns a list of all cells that are reachable from the Cell at the given position, that also share the same value and colour.
		"""
		cell = self.getCellAt( pos )
		valid = [c for c in self.getCellType( END ) if c.getValue() == cell.getValue() and c.getId() != cell.getId() and c.getPosition() != cell.getPosition() and c.colour == cell.colour and self.isReachable( pos, c.getPosition() )]
		return filter( lambda c : len(self.getConnections( pos, c.getPosition() )) > 0, valid )
		
	def getCellType( self, cellType ):
		"""Returns all the cells of a particular type.
			Cell Types:
				END		- The cell is an endpoint, and is visible in the initial puzzle state.
				PATH	- The cell contains a value, but is a part of a path connecting two endpoints.
				EMPTY	- The cell contains no data, and represents a blank space in the puzzle.
		"""
				
		return [c for c in self.cellList if c.getType() == cellType]

		
	def setInitEndCellCount( self ):
		self.initEndCells = self.getConnectableEndCellCount()
		
	def numConnected( self ):
		"""Returns the number of unique connected paths in the current puzzle configuration.
		"""
		sids = [c.startId for c in self.getCellType( PATH )]
		eids = [c.endId for c in self.getCellType( PATH )]
		return len( set( sids + eids ))
		
	def getConnectedness( self ):
		"""Returns the percentage of the board that has been fully connected.
		"""
		connectedCells = self.numConnected()
		return connectedCells/float( len( self.getCellType( END )) + connectedCells )
		
	def getConnectableEndCellCount( self ):
		return len( filter( lambda x: x.getValue() > 2, self.getCellType( END )))
		
	def getCompleteness( self ):
		return ( self.initEndCells - self.getConnectableEndCellCount()) / float( self.initEndCells )
		
	def getConnections( self, startPos, endPos ):
		"""Returns the set of valid connection patterns for a given pair of endpoints.
		"""
		# Get the cells at the specified positions.
		startCell = self.getCellAt( startPos )
		endCell = self.getCellAt( endPos )
		
		# There are no valid connections if the two cells are:
		#	1) Not of equal value,
		if startCell.getValue() != endCell.getValue(): return []
		
		#	2) Not both end cells,
		if startCell.getType() == PATH or endCell.getType() == PATH: return []
		
		#	3) Not reachable from one another.
		if not self.isReachable( startPos, endPos ): return []

		valid = []
		value = startCell.getValue()
		
		# Get the possible paths for the specified value.
		distance = getEuclidianDistance( startCell.getPosition(), endCell.getPosition() )
		
		# If the connection set has been used before, no need to rotate
		if self.pathList.isMirrored( value, distance ):
			paths = self.pathList.paths[value][distance]
		else:
			paths = addMirrors( self.pathList.paths[value][distance] )
			self.pathList.paths[value][distance] = paths
			self.pathList.addMirrored( value, distance )
		
		# Test whether each path is a valid connector of the two points:
		#  For each of the possible paths,
		for p in paths:
		
			# All the possible rotations are expanded, and for each one,
			plist = getRotations( p )
			for rp in plist:
			
				# The alignment of the rotation is checked (it's endpoints correspond to the positions of the specified points).
				if rp[-1] == getRelativePos( startPos, endPos ) or rp[-1] == getRelativePos( endPos, startPos ):
				
					# If the starting position of the rotation is not the specified start position, the rotation is reversed.
					p = rp if rp[-1] == getRelativePos( startPos, endPos ) else getRelativePath( rp )
					isValid = True
					
					# Each of the positions in the path being tested is checked for any properties that render it invalid:
					for pos in p:
						aPos = getAbsolutePos( startPos, pos )
						
						# The position must be in bounds, and either empty (not a path point or end point in another path), or
						#  one of the initially specified end points.
						if not self.isValidPos( aPos ) or (self.getCellAt( aPos ).getType() != EMPTY and self.getCellAt( aPos ).getId() != startCell.getId() and 0 < p.index( pos ) < len(p)-1):
							isValid = False
							break
						
					if isValid and p not in valid: valid.append( p )
						
		return valid
		
	def innerConnect( self, startPos, endPos, path ):
		"""Helper function for self.connect.
		Updates the values of all the cells in a newly connected path.
		"""
		startCell = self.getCellAt( startPos )
		endCell = self.getCellAt( endPos )
	
		startCell.connected = True
		endCell.connected = True
		
		for pos in path:
			cell = self.getCellAt( getAbsolutePos( startPos, pos ))
			cell.setType( PATH )
			cell.setValue( startCell.getValue() )
			cell.startId = startCell.cid
			cell.endId = endCell.cid
			cell.colour = startCell.colour
			
	def connect( self, startPos, endPos, path ):
		"""Connects a given pair of endpoints with a specified path.
		"""
		oldGrid = self.getCellInfo()
		self.innerConnect( startPos, endPos, path )
		newGrid = self.getCellInfo()
		self.setCellInfo( oldGrid )
		return Grid( self.dimensions[X], self.dimensions[Y], newGrid )
	
		
	def getSimple( self ):
		"""Gets the list of unconnected end point cells that have only one possible connecting cell.
		"""
		# Get cells with only one possible connecting cell.
		cells = filter( lambda cell: len( self.getReachable( cell.getPosition() )) == 1, self.cellList )
	
		uniqueCells = []
		# Remove matching cells (one cell per pair).
		for c in cells: uniqueCells.append( c ) if self.getReachable( c.getPosition() )[0] not in uniqueCells else None
		
		# Reduce set to cells with only one possible connecting path.
		validCells = filter( lambda cell: len( self.getConnections( cell.getPosition(), self.getReachable( cell.getPosition() )[0].getPosition() )) == 1, uniqueCells )
		
		return [c.getPosition() for c in validCells]
		
	def solveSimple( self ):
		"""Uses self.getSimple() to repeatedly connect unconnected endPoints, and then update the grid
		based on the results to further narrow down the possible connections that can be made.
		"""
		simple = self.getSimple()
		
		while simple:
			for pos in simple:
				if self.getCellAt( pos ).getType() != END or not self.getReachable( pos ): continue
				target = self.getReachable( pos )[0].getPosition()
				conns = self.getConnections( pos, target )
				self.innerConnect( pos, target, conns[0] )
				
			simple = self.getSimple()
			
	
	def backtrack( self ):
		# Solve straightforward connections
		self.solveSimple()
		
		# Initialize stack
		stack = []
		
		while self.getCompleteness() < 1:
			# Update available moves
			uniqueCells = []
			cells = filter( lambda cell: len( self.getReachable( cell.getPosition() )) == 1, self.cellList )
			for c in cells: uniqueCells.append( c ) if self.getReachable( c.getPosition() )[0] not in uniqueCells else None
			freeCells = { tuple(c.getPosition()) : self.getConnections( c.getPosition(), self.getReachable( c.getPosition() )[0].getPosition() ) for c in uniqueCells }
			
			# If no more moves, solver is finished
			if not freeCells:
				return -1
			
			# Select a move
			pos = list( choice( freeCells.keys() ))
			cell = self.getCellAt( pos )			
			reachable = self.getReachable( pos )

			target = reachable[0].getPosition()
			conns = freeCells[tuple(pos)]
			shuffle( conns )
			conn = conns.pop()

			# If not a valid move, backtrack 
			if not conns:
				# Pop previous frame from stack
				frame = stack.pop()
				grid = frame[GRID]
				
				# Reset available possibilities
				freeCells.pop( tuple(pos) )
				
			else: freeCells[tuple(pos)] = conns
			
			# Make connection
			self.innerConnect( cell.getPosition(), target, conn )
			
			# Save frame to stack
			stack.append( deepcopy( self.grid ) )
		
	
g = SolveGrid( int(sys.argv[XSIZE]), int(sys.argv[YSIZE]) )
fname, ftype = sys.argv[FILENAME].split('.')

g.importGrid( fname, ftype )
g.setInitEndCellCount()
g.backtrack()
g.exportGrid( fname, ftype )

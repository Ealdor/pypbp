"""
	generator.py (RENAME)
	~~~~~~~~~

	Generator for G52GRP Link-A-Pix Project
	
	This module implements the puzzle generation functionality for a given image bitmap.
	The program takes 3 arguments on the command line, and outputs a valid puzzle to a
	temp file (of name and type specified in constants.py) in the specified puzzle directory.
	
	Command line interface:
		$ python generator.py [PUZZLE_WIDTH] [PUZZLE_HEIGHT] [PUZZLE_NAME] [PUZZLE_DIFFICULTY (4-10)]
		(PUZZLE_NAME is a type-specified name of a file located in the directory specified in constants.py)
		
	:Mandla Moyo, 2014.
"""


from math import pi, cos, sin
from random import randint, choice
from pattern import getRelativePos, getAbsolutePos, getRotations, getRelativePath, getEuclidianDistance, addMirrors
from constants import *
from grid import Grid
from cellReader import Cell
from copy import deepcopy
import sys

class GenerateGrid( Grid ):
	def __init__( self, x, y, limit ):
		Grid.__init__( self, x, y, limit )
		self.pids = 1
		self.runs = 0
		self.build()
		
	def build( self ):
		self.grid = [[ INIT_VALUE for c in range( self.dimensions[X] )] for r in range( self.dimensions[Y] )]
	
	def getAllCells( self ):
		cells = []
		for j in range(len(self.grid)):
			for i in range(len(self.grid[j])):
				c = self.grid[j][i]
				cells.append(c)
				
		return cells
		
	def getCellList( self ):
		cells = []
		for j in range(len(self.grid)):
			for i in range(len(self.grid[j])):
				c = self.grid[j][i]
				cells.append( Cell( [c[X],c[Y]] ))
				cells[-1].setInfo( c[PID], c[VALUE], c[TYPE], colour = c[COLOUR] )
				if c[TYPE] != END: cells[-1].setInfo( c[PID], 0, EMPTY )
		return cells
	
	def setCellInfo( self, cellInfo ):
    
		for info in cellInfo:
			self.grid[info[Y]][info[X]] = [info[X],info[Y],info[VALUE],info[TYPE],self.pids, self.pids, info[COLOUR]]
			self.pids += 1


	def getNeighbors( self, pos ):
		neighbors = []
		
		for y in range(-1,2):
			for x in range(-1,2):
				p = [pos[X] + x, pos[Y] + y]
				if( self.isValidPos( p )) and abs(x) != abs(y):
					neighbors.append( self.grid[p[Y]][p[X]] )
		
		return neighbors
	
	def getEndNodes( self, value ):
		nodes = []
		for y in range(len(self.grid)):
			for x in range(len(self.grid[y])):
				n = self.grid[y][x]
				if n[TYPE] == END and (value == ANY_VALUE or n[VALUE] == value):
					nodes.append( n )
					
		return nodes
		
	def getRandomPair( self, value ):
		"""Returns a pair of adjacent nodes with the same colour and type, whose
		combined value is under a pre-set limit.
		"""
		# First node must be an END node with a value under the limit
		nodes = filter( lambda x: x[VALUE] < self.limit, self.getEndNodes( value ))
		if len( nodes ) < MINIMUM_NODECOUNT: return UNDERPOPULATION_ERROR
		first = choice(nodes)
		
		# Second node has same constraints as first, but summed value rather than individual
		neighbors = filter( lambda x: 0 < x[VALUE] + first[VALUE] <= self.limit and x[TYPE] == END and x[COLOUR] == first[COLOUR], self.getNeighbors(first[:2]))
		if neighbors == EMPTY_LIST: return NO_MATCH_ERROR
		second = choice(neighbors)

		return [first,second]
		
	def getConnectedNeighbors( self, pos, pid ):
		"""Given a cell's position and it's ID number, this function returns any
		neighboring cells with the same ID.
		"""
		return filter( lambda x: x[PID] == pid, self.getNeighbors( pos ))
		
	
	def getConnected( self, node, value, oldId, newId ):
		"""Recursive function used to update the values of all the cells in a
		given path.
		"""
		
		# Start with PATH nodes, then move onto END nodes, to ensure correct traversal order (nodes with fewest neighbours go first)
		# Only considers those nodes in path yet to be updated as valid neighbours (with the old ID)
		neighbors = sorted( self.getNeighbors(node[:2]), key=lambda x: (-x[TYPE], len(self.getConnectedNeighbors(x[:2],oldId))))
		
		node[VALUE],node[PID] = value, newId
		for neighbor in neighbors:
		
			# If a connected neighbour exists, the current node is a path node
			if neighbor[PID] == oldId: 
				node[TYPE] = PATH
				return self.getConnected( neighbor, value, oldId, newId )
		
		return node

	def merge( self, value=ANY_VALUE ):
		"""Finds a valid random pair of cells, and merges their two paths to become a
		new path whose value is the sum of the initial two cell's values.
		"""

		# Search for a valid pair until a valid pair is found, or max attempts are reached.
		attempts = MAX_ATTEMPTS 
		pair = self.getRandomPair( value )
		while type(pair) is int or pair[FIRST][PID] == pair[SECOND][PID]:
			if (type(pair) is int and pair > 0) or attempts == 0: return NO_MATCH_ERROR
			pair = self.getRandomPair( value )
			attempts -= 1
		
		# Set values for new path
		newValue = pair[FIRST][VALUE] + pair[SECOND][VALUE]
		newId = self.pids
		self.pids += 1
		
		# Save the current grid configuration in case merge is invalid
		temp = deepcopy( self.grid )
		fail = False
		ends = [] # This list will hold the endpoints of the new path
		
		# For each of the paired cells, update it's path with the new values
		for n in pair:
			oldId = n[PID]
			ends.append( self.getConnected( n, newValue, oldId, newId ))
		
		# Find all valid connections the path's endpoints can make
		allPaths = self.getConnections( ends[FIRST], ends[SECOND] )
		
		# Check if ends can both connect to more than one other node. If so, fail.
		#  Preserves puzzle's unique solve-ability.
		if self.getReachable( ends[FIRST] ) and self.getReachable( ends[SECOND] ): fail = True
		
		# Check to make sure the created path doesn't overlap with any non-empty cells.
		if not fail:
			for path in allPaths:
				for p in path:
					if self.grid[ends[FIRST][Y]+p[Y]][ends[FIRST][X]+p[X]][TYPE] == EMPTY:
						fail = True

		if fail:
			# Reset the grid to the old configuration
			self.grid = temp
			
			# Add another merge run with 50% likelihood
			self.runs += randint(0,1)
			
			# Return end pairs and error message
			return MERGE_ERROR
				
		return True
		
	def getRuns( self, x, y, lim ):
		"""Determines how many merge operations should be run on a given puzzle,
		dependent on the puzzle's dimensions and maximum value limit.
		"""
		return int( (x*y)/((LIMIT_CONSTANT/lim)*10) )
		
	
	def isReachable( self, p1, p2 ):
		"""Returns True if p1 reachable from p2 and visa versa.
		"""
		res = abs( p1[X]-p2[X] ) + abs( p1[Y] - p2[Y] )
		v = p1[VALUE]

		return res < v and res%2 != v%2
	
	
	def getReachable( self, cell ):
		cells = self.getAllCells()
		valid = [c for c in cells if c[TYPE] == END and c[VALUE] == cell[VALUE] and c[PID] != cell[PID] and c[COLOUR] == cell[COLOUR] and self.isReachable( cell, c )]
		return filter( lambda c : len(self.getConnections( cell, c )) > 0, valid )
		
		
	def runMerges( self, xsize, ysize, limit ):
		self.runs = self.getRuns( xsize, ysize, limit )
		
		## PROGRESS DISPLAY FOR COMMAND LINE ##
		inc = self.runs/10
		if self.runs > 100: inc = self.runs/100
		cur = 0
		print self.runs, xsize*ysize
		#######################################
		
		while self.runs > 0:
			self.runs -= 1
			self.merge()
			
			## PROGRESS DISPLAY FOR COMMAND LINE ##
			cur += 1
			if cur > inc: 
				print ".",
				sys.stdout.flush()
				cur = 0
			#######################################
			

		
	def getConnections( self, startCell, endCell ):
		# Error checking
		if startCell[VALUE] != endCell[VALUE]: return []
		if startCell[TYPE] == PATH or endCell[TYPE] == PATH: return []
		if not self.isReachable( startCell, endCell ): return []
		
		# Get positions from cell values
		startPos = [startCell[X],startCell[Y]]
		endPos = [endCell[X],endCell[Y]]
		value = startCell[VALUE]
		valid = []
		
		# Get the possible paths for the specified value.
		distance = getEuclidianDistance( startPos, endPos )
		
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
						apos = getAbsolutePos( startPos, pos )
						if not (0 <= apos[X] < self.dimensions[X] and 0 <= apos[Y] < self.dimensions[Y]):
							isValid = False
							break
							
						cell = self.grid[apos[Y]][apos[X]]
						
						# if a cell in the specified path is not either empty, or a part of the defined path, it is invalid
						if cell[TYPE] != EMPTY and cell[PID] != startCell[PID] and 0 < p.index( pos ) < len(p)-1 :
							isValid = False
							break
						
					if isValid and p not in valid: valid.append( p )
						
		return valid
		

xsize, ysize, filename, limit = int(sys.argv[XSIZE]), int(sys.argv[YSIZE]), sys.argv[FILENAME], int(sys.argv[LIMIT])

g = GenerateGrid( xsize, ysize, limit )
fname, ftype = filename.split('.')
g.importGrid( fname, ftype )
g.runMerges( xsize, ysize, limit )
g.exportGrid( fname, ftype )

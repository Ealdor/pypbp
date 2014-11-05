"""
	pattern.py
	~~~~~~~~~

	This module implements the functions used to generate the possible unique connection
	types between two cells of any given value and distance. The resulting set of patterns
	is then stored in the pathContainer class.

	:Mandla Moyo, 2014.
"""

from math import sin, cos, pi, ceil, sqrt

X = 0
Y = 1

def mirror( pos, axis=0 ):
	"""For a given coordinate pair, returns its mirror along a specified axis.
	"""
	newPos = pos[:]
	newPos[axis] *= -1
	return newPos
		
def mirrorPath( path, axis=0 ):
	return [mirror(pos,axis) for pos in path]

def rotate( pos, angle ):
	"""Rotates a coordinate pair counter-clockwise by a given angle in radians.
	"""
	return [ int(round(pos[X]*cos( angle ) - pos[Y]*sin( angle ))), int(round(pos[X]*sin( angle ) + pos[Y]*cos( angle ))) ]
	
def rotatePath( path, angle=pi/2 ):
	return [ rotate( pos, angle ) for pos in path ]
	
def getRotations( path ):
	"""Returns a list containing a specified path rotated by 0, 90, 180, and 270 degrees.
	"""
	return [ rotatePath( path, (pi/2)*i ) for i in range(4) ]

def getRelativePos( origin, pos ):
	"""Returns the position of a point relative to a specified origin.
	"""
	return [pos[X] - origin[X], pos[Y] - origin[Y]]

def getAbsolutePos( origin, pos ):
	"""Takes an origin, and a position relative to that origin, and returns the equivalent
	position relative to a [0,0] origin.
	"""
	return [origin[X] + pos[X], origin[Y] + pos[Y]]
	
def getRelativePath( path ):
	"""Returns the positions of all the points in a given path relative
	to the position of the first point in the path.
	"""
	tempPath = path[:]
	tempPath.reverse()
	return [getRelativePos(tempPath[0],pos) for pos in tempPath]
	
def getManhattanDistance( p1, p2 ):
	"""Returns the Manhattan distance of two points, which is the sum of
	the absolute difference of the x and y coordinate values.
	"""
	return abs(p1[X] - p2[X]) + abs(p1[Y] - p2[Y])
	
def getEuclidianDistance( p1, p2 ):
	return int( ceil( sqrt( abs(p1[X]-p2[X])**2 + abs(p1[Y]-p2[Y])**2 )))
	
def getPathExtensions( path ):
	"""For a given path, returns all the valid, unique ways in which an
	additional point can be added to the path.
	"""
	exts = []
	for i in range(-1,2):
		for j in range(-1,2):
			if abs(i) + abs(j) == 1:
				newPath = path[:]
				newPos = [ newPath[-1][X] + i, newPath[-1][Y] + j ]
				if newPos not in newPath and newPos[X] >= 0 and newPos[Y] >= 0:
					newPath.append( newPos )
					exts.append( newPath )

	return exts

def addMirrors( pathList ):
	newPathList = []
	for path in pathList:
		mPath = mirrorPath( path )
		
		if mPath == path: newPathList.append( path )
		else: newPathList.extend( [path, mPath] )
	
	return newPathList
	
def remDups( plist ):
	"""Removes all duplicates from a list of paths.
	"""
	dots = 0
	progress = 0
	normalizedPathWorth = 100/float(len(plist))
	uq = []
	while plist:
		while dots < ceil(progress):
			dots += 1
			print ".",
			
		
		pp = plist.pop()
		if pp not in uq: uq.append( pp )
		

		progress += normalizedPathWorth
		
	print ""
	return [pt.pattern for pt in uq]
	
def getDistanceMap( li ):
	dmap = {}
	for p in li:
		d = getEuclidianDistance( p[0], p[-1] )
		if d in dmap: dmap[d].append( p )
		else: dmap[d] = [p]
	
	return dmap
	
def getUniquePaths( length ):
	"""For the given length, returns a list of all unique possible paths
	containing that number of nodes. 
		Valid: no intersections.
		Unique: pattern is not repeated (includes all rotations and mirroring).
	"""
	print "Starting.."
	p = genPaths( length )
	print "Paths generated. Extracting patterns.."
	pl = getPatternList( p )
	print "Patterns extracted. Removing duplicates.."
	nodups = remDups( pl )
	print "Duplicates removed, operation complete"
	dmap = getDistanceMap( nodups )
	return dmap
	
def printPath( path ):
	size = len(path)
	for j in range(size):
		for i in range(size):
			if [i,j] in path: print 'X',
			else: print ' ',
		print ''
	print ''
	
				
def genPaths( length ):
	"""Generates a list of all possible (valid) paths of a given length,
	with no regard to duplicates.
	"""
	pathList = [ [[0,0]] ]
	while( len( pathList[0] ) < length ):
		newPathList = []
		for path in pathList:
			newPaths = getPathExtensions( path )
			newPathList.extend( newPaths )
		
		pathList = newPathList
	return pathList
	
def getPatternList( paths ):
	"""Converts path list to Pattern structures
	"""
	patterns = [Pattern( path ) for path in paths]
	return patterns

	
class Pattern:
	"""The Pattern class is used to allow operator comparison of paths
	to enforce path validity and uniqueness.
	"""
	def __init__( self, pattern ):
		self.pattern = pattern
		
	def __eq__( self, other ):
		matchPattern = other.pattern[:]
		rot = getRotations( matchPattern )
		mrot = getRotations( mirrorPath( matchPattern ))
		
		pt = self.pattern
		rpt = getRelativePath( pt )
		
		if pt in rot or pt in mrot or rpt in rot or rpt in mrot: return True
		return False
		
	def __ne__( self, other ):
		return not self.__eq__( other )
		
		

"""
	fileReader.py
	~~~~~~~~~

	This module implements a basic file I/O, creating a standard interface
	for either json or csv files.

	:Mandla Moyo, 2014.
"""

import json
import csv
import os
import constants

class FileReader():
	"""The base FileReader class simply controls directory
	management and error handling
	"""
	def __init__( self, directory ):
		if not os.path.isdir( directory ): raise IOError( "Directory '" + directory + "' does not exist" )
		self.directory = directory
		self.fileType = None
		
	def changeDirectory( self, newDirectory ):
		if not os.path.isdir( newDirectory ): raise IOError( "Directory '" + newDirectory + "' does not exist" )
		self.directory = newDirectory
		
	def readFile( self, name ):
		return None
		
	def writeFile( self, name ):
		pass
		
		
class CsvReader( FileReader ):
	"""CSVReader simply reads from or writes to a specified csv file, without
	any particular formatting or alteration of the handled data.
	"""
	def __init__( self, directory ):
		FileReader.__init__( self, directory )
		self.fileType = ".csv"
		
	def readFile( self, name ):
		data = []
		filepath = self.directory + name + self.fileType
		if not os.path.isfile( filepath ): raise IOError( "File '" + filepath + "' does not exist" )
					
		with open( filepath, 'rb' ) as f:
			reader = csv.reader(f)
			for row in reader:
				data.append([int(value) for value in row])
									
		return data

	def writeFile( self, name, data ):
		"""Takes a filename, and a 2d array containing the rows
		of data to be written.
		"""
		filepath = self.directory + constants.OUTPUT_FILENAME_GENERATOR + self.fileType
		with open( filepath, 'w') as outfile:
			writer = csv.writer( outfile )
			writer.writerows( data )
		
		
class JsonReader( FileReader ):
	"""JsonReader simply reads from or writes to a specified json file, without
	any particular formatting or alteration of the handled data.
	"""
	def __init__( self, directory ):
		FileReader.__init__( self, directory )
		self.fileType = ".json"
		
	def readFile( self, name ):
		filepath = self.directory + name + self.fileType
		if not os.path.isfile( filepath ): raise IOError( "File '" + filepath + "' does not exist" )
		
		json_data = open( filepath )
		data = json.load( json_data )
		json_data.close()
		return data
		
	def writeFile( self, name, data ):
		"""Takes a filename, and a 2d array containing the rows
		of data to be written.
		"""
		filepath = self.directory + constants.OUTPUT_FILENAME_GENERATOR + self.fileType
		with open( filepath, 'w' ) as outfile:
			json.dump( data, outfile )
		

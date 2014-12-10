# -*- coding: utf-8 -*-

###############################################################################
## Copyright (C) 2014 Jorge Zilbermann ealdorj@gmail.com
##
##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################

import math
import string
import pickle

ncolumns = 0
nrows = 0

def euclide(dire, dire2):
	return abs( int(round(math.sqrt( (dire[0] - dire2[0])**2 + (dire[1] - dire2[1])**2 ))))

def write_file(table_all):
	f = open("temp.csv", 'w')
	for x in xrange(0, nrows):
		for y in xrange(0, ncolumns):
			if table_all[y][x].get('number') == -1:
				f.write('0')
			else:
				f.write(str(table_all[y][x].get('number')))
			if y == ncolumns-1: f.write('\n')
			else: f.write(',')

	with open("temp.pickle", 'wb') as f:
		pickle.dump(table_all, f)

def read_file(fname):
	global ncolumns, nrows

	try:
		f = open(fname, 'r')
	except IOError:
		print "File not found"
		sys.exit()

	contador = 0
	ncolumns = len(string.split(string.strip(f.readline()), ','))
	f.seek(0)
	for linea in f.xreadlines( ): contador+= 1
	nrows = contador
	f.seek(0)

	table_all = [[None for y in xrange(0, int(nrows))] for x in xrange(0, int(ncolumns))]

	for x in xrange(0, int(nrows)):
		num = string.split(string.strip(f.readline()), ',')
		for y in xrange(0, int(ncolumns)):
			tn = int(string.split(num.pop(0), ',')[0])
			if tn == 0:
				table_all[y][x] = {'number': 0, 'posicion': (y, x), 'conn': [], 'ps': 0}
			elif tn == 1:
				table_all[y][x] = {'number': 1, 'posicion': (y, x), 'conn': [], 'ps': 1, 'c': False}

	return table_all
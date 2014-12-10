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
import json

ncolumns = 0
nrows = 0

def euclide(dire, dire2):
	return abs( int(round(math.sqrt( (dire[0] - dire2[0])**2 + (dire[1] - dire2[1])**2 ))))

def write_csv(table_all):
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

def write_json(table_all):
	f = open("temp.json", 'w')
	rows = []
	for x in xrange(0, nrows):
		cols = []
		for y in xrange(0, ncolumns):
			if table_all[y][x].get('number') == 0 or table_all[y][x].get('number') == -1:
				color = [255, 255, 255]
				number = 0
			else:
				color = table_all[y][x].get('color')
				number = table_all[y][x].get('number')
			cols.append({'color':{'r':color[0],'b':color[2],'g':color[1]},'number':number})
		rows.append(cols)
	json.dump(rows, f)

	with open("temp_color.pickle", 'wb') as f:
		pickle.dump(table_all, f)

def read_csv(fname):
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
			table_all[y][x] = {'number': tn, 'posicion': (y, x), 'conn': [], 'ps': tn, 'c': False, 'color': (0, 0, 0)}

	return table_all

def read_json(fname):
	global ncolumns, nrows

	try:
		f = open(fname, 'r')
	except IOError:
		print "File not found"
		sys.exit()

	contador = 0
	data = json.load(f)
	for row in xrange(len(data)):
		for col in xrange(len(data[row])):
			contador += 1
		break
	nrows = len(data)
	ncolumns = contador
	f.seek(0)

	table_all = [[None for y in xrange(0, int(nrows))] for x in xrange(0, int(ncolumns))]

	data = json.load(f)
	for row in xrange(len(data)):
		for col in xrange(len(data[row])):
			value = data[row][col]["number"]
			c = data[row][col]["color"]
			colour = [c["r"], c["g"], c["b"]]
			table_all[col][row] = {'number': value, 'posicion': (col, row), 'conn': [], 'ps': 1, 'c': False, 'color': colour}
	
	return table_all

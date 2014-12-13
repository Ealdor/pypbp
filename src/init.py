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

import json
import sys
import string
import pygame
from cells import *

def init_pygame():
	""" Función inicializar los modulos de pygame necesarios """

	pygame.font.init()

def init_puzzle(fname):
	""" Inicializa el tablero desde un archivo pasado

	Args:
		fname(string): nombre del fichero

	Returns:
		ncolumns(string): numero de columnas del puzzle
		nrows(string): numero de filas del puzzle
		table(list): tabla del puzzle

	"""
	
	# ABRIR ARCHIVO
	try:
		f = open(fname, 'r')
	except IOError:
		print "File not found"
		sys,exit()

	typef = fname.rsplit('.')[-1]

	# CONTEO DE COLUMNAS Y FILAS
	if typef == 'csv':
		contador = 0
		ncolumns = len(string.split(string.strip(f.readline()), ','))
		f.seek(0)
		for linea in f.xreadlines( ): contador+= 1
		nrows = contador
	elif typef == 'json':
		contador = 0
		data = json.load(f)
		for row in xrange(len(data)):
			for col in xrange(len(data[row])):
				contador += 1
			break
		nrows = len(data)
		ncolumns = contador
	f.seek(0)

	# INICIALIZACION DE LA TABLA
	table = [[Cell(x*CELL_WIDTH, y*CELL_WIDTH, 0) for y in xrange(0, int(nrows))] for x in xrange(0, int(ncolumns))]

	# PARSEO DE LOS ARCHIVOS
	if typef == 'csv': # CSV
		for x in xrange(0, int(nrows)):
			num = string.split(string.strip(f.readline()), ',')
			for y in xrange(0, int(ncolumns)):
				tn = int(string.split(num.pop(0), ',')[0])
				if tn != 0:
					table[y][x] = Cell(y*CELL_WIDTH, x*CELL_WIDTH, tn, BLACK)
	elif typef == 'json': # JSON
		data = json.load(f)
		for row in xrange(len(data)):
			for col in xrange(len(data[row])):
				value = data[row][col]["number"]
				c = data[row][col]["color"]
				colour = [c["r"], c["g"], c["b"]]
				table[col][row] = Cell(col*CELL_WIDTH, row*CELL_WIDTH, value, colour)
	f.close()
	return ncolumns, nrows, table
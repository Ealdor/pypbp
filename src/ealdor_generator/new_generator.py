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

''' Lógica del generador:
		- Elegir pixel aleatorio del archivo que este libre (no haya camino definido) y sea un numero distinto de cero.
		- Elegir aleatoriamente dirección libre y no marcada (no haya sido elegida para este camino antes).
		- Comprobar si el puzzle está bien generado:
				- COND1: si desde un número se llega a uno igual (sin ser pareja) y desde la pareja del último se llega al primero.
				- COND2: si mediante cuandros blancos hay mas de un camino posible desde un número a su pareja.
		- Por cada fallo volver al paso 1 (menos el número problemático). Si no hay fallos se ha terminado. '''

import sys
import pygame
import string
import random

def random_dir(table_uno, pstart):
	mov = {'up': None, 'down': None, 'left': None, 'right': None, 'stay': pstart}
	
	try: mov['up'] = table_uno.index((pstart[0], pstart[1]-1))
	except: pass
	try: mov['down'] = table_uno.index((pstart[0], pstart[1]+1))
	except: pass
	try: mov['left'] = table_uno.index((pstart[0]-1, pstart[1]))
	except: pass
	try: mov['right'] = table_uno.index((pstart[0]+1, pstart[1]))
	except: pass	
	
	aux = random.choice(mov.keys())
	while mov.get(aux) == None:
		aux = random.choice(mov.keys())
	print "movimiento: " + aux
	return mov.get(aux)

def step_two(table_uno, pstart):
	""" Elegir aleatoriamente dirección libre y no marcada (no haya sido elegida para este camino antes)."""
	
	print "principio: {0}".format(pstart)
	history = []

	aux = random_dir(table_uno, pstart)

	history.append(pstart)
	if aux != pstart:
		print "nos movemos a: {0}".format(table_uno[aux])
		history.append(table_uno[aux])
		pstart = table_uno[aux]
		table_uno.pop(aux)

	while aux != pstart:
		print "punto partida: {0}".format(pstart)
		aux = random_dir(table_uno, pstart)
		if aux == pstart:
			break
		print "nos movemos a: {0}".format(table_uno[aux])
		history.append(table_uno[aux])
		pstart = table_uno[aux]
		table_uno.pop(aux)
	
	print "final: {0}".format(aux)
	return history

def step_one(table_all, table_uno):
	""" Elegir pixel aleatorio del archivo que este libre (no haya camino definido) y sea un numero distinto de cero. """

	while len(table_uno) > 0:
		ran = random.randint(0, len(table_uno)-1)
		changes = step_two(table_uno, table_uno.pop(ran))

		prin = changes[0]
		ter = changes[-1]
		print prin, ter

		for change in changes:
			for x in table_all:
				for y in x:
					for key in y:
						if key == 'posicion':
							if change == y[key]:
								if  prin == y[key] or ter == y[key]:
									y['number'] = len(changes)
								else:
									y['number'] = 0

def write_file(table_all, ncolumns, nrows):
	f = open("temp.csv", 'w')
	for x in xrange(0, nrows):
		for y in xrange(0, ncolumns):
			f.write(str(table_all[y][x].get('number')))
			if y == ncolumns-1: f.write('\n')
			else: f.write(',')

if __name__ == "__main__":
	try:
		f = open(sys.argv[1], 'r')
	except IOError:
		print "File not found"
		sys,exit()

	typef = sys.argv[1].split('.')[1]

	# CONTEO DE COLUMNAS Y FILAS
	if typef == 'csv':
		contador = 0
		ncolumns = len(string.split(string.strip(f.readline()), ','))
		f.seek(0)
		for linea in f.xreadlines( ): contador+= 1
		nrows = contador
		f.seek(0)

	table_all = [[None for y in xrange(0, int(nrows))] for x in xrange(0, int(ncolumns))]
	table_uno = []

	if typef == 'csv': # CSV
		for x in xrange(0, int(nrows)):
			num = string.split(string.strip(f.readline()), ',')
			for y in xrange(0, int(ncolumns)):
				tn = int(string.split(num.pop(0), ',')[0])
				if tn == 0:
					table_all[y][x] = {'number': 0, 'posicion': (y, x)}
				else:
					table_all[y][x] = {'number': 1, 'posicion': (y, x)}
					table_uno.append((y, x))

	step_one(table_all, table_uno)
	write_file(table_all, ncolumns, nrows)

	sys.exit()
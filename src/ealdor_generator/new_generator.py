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

fails = 0

def findfinal(table_all, dire, ini, allini):
	global fails

	if dire[0] >= 0 and dire[1] >= 0:
		for x in table_all:
			for y in x:
				if y.get('number') == allini.get('number') and y.get('posicion') == dire and y.get('posicion') != ini:
					# print "fin: {0}".format(dire)
					fails +=1
					if fails == 2:
						return True
	return False

def find(table_all, dire, ini, allini):
	if dire[0] >= 0 and dire[1] >= 0:
		for x in table_all:
			for y in x:
				if (y.get('number') == 0 or y.get('posicion') in allini.get('conn')) and (y.get('posicion') == dire) and y.get('posicion') != ini and y.get('posicion') != allini.get('conn')[-1]:
					#print "camino: {0}".format(dire)
					return True
	return False

def recursive(table_all, ini, allini, dire):
	if find(table_all, dire, ini, allini):
		return [(dire[0], dire[1]-1), (dire[0]+1, dire[1]), (dire[0], dire[1]+1), (dire[0]-1, dire[1])]
	else:
		return []

def way_mov(table_all, ini, allini):
	global fails
	fails = 0

	aux = [(ini[0], ini[1]-1), (ini[0]+1, ini[1]), (ini[0], ini[1]+1), (ini[0]-1, ini[1])]

	for dire in aux:
		for dire2 in recursive(table_all, ini, allini, dire):
			if allini.get('number') > 3:
				for dire3 in recursive(table_all, ini, allini, dire2):
					if allini.get('number') > 4:
						for dire4 in recursive(table_all, ini, allini, dire3):
							if allini.get('number') > 5:
								for dire5 in recursive(table_all, ini, allini, dire4):
									if allini.get('number') > 6:
										for dire6 in recursive(table_all, ini, allini, dire5):
											if allini.get('number') > 7:
												for dire7 in recursive(table_all, ini, allini, dire6):
													if allini.get('number') > 8:
														for dire8 in recursive(table_all, ini, allini, dire7):
															if allini.get('number') > 9:
																for dire9 in recursive(table_all, ini, allini, dire8):
																	if allini.get('number') > 10:
																		for dire10 in recursive(table_all, ini, allini, dire9):
																			if findfinal(table_all, dire10, ini, allini): return True
																	else:
																		if findfinal(table_all, dire9, ini, allini): return True		
															else:
																if findfinal(table_all, dire8, ini, allini): return True
													else:
														if findfinal(table_all, dire7, ini, allini): return True
											else:
												if findfinal(table_all, dire6, ini, allini): return True
									else:
										if findfinal(table_all, dire5, ini, allini): return True	
							else:
								if findfinal(table_all, dire4, ini, allini): return True
					else: 
						if findfinal(table_all, dire3, ini, allini): return True
			else:
				if findfinal(table_all, dire2, ini, allini): return True

	return False

def cond_dos(table_all):
	""" COND2: si mediante cuandros blancos o su propio camino hay mas de un camino posible desde un número a su pareja. """

	print "Paso 2: Buscando y corrigiendo posibles fallos:",
	sys.stdout.flush()

	aux = []

	for x in table_all:
		for y in x:
			if y.get('number') > 2 and len(y.get('conn')) > 0:
				#print "Pixel: {0}, {1}".format(y.get('number'), y.get('conn'))
				if way_mov(table_all, y.get('posicion'), y):
					pos = y.get('posicion')
					con = y.get('conn')
					for w in con:
						aux.append(w)

	for w in aux:
		table_all[w[0]][w[1]]['number'] = 1
		table_all[w[0]][w[1]]['conn'] = []

	return aux

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
	# if aux == 'stay':
	# 	aux = random.choice(mov.keys())
	while mov.get(aux) == None:
		aux = random.choice(mov.keys())
		# if aux == 'stay':
		# 	aux = random.choice(mov.keys())
	#print "movimiento: " + aux
	return mov.get(aux)

def step_two(table_uno, pstart):
	""" Elegir aleatoriamente dirección libre y no marcada (no haya sido elegida para este camino antes). """
	
	#print "principio: {0}".format(pstart)
	history = []

	aux = random_dir(table_uno, pstart)

	history.append(pstart)
	if aux != pstart:
		#print "nos movemos a: {0}".format(table_uno[aux])
		history.append(table_uno[aux])
		pstart = table_uno[aux]
		table_uno.pop(aux)

	while aux != pstart and len(history) < 11:
		#print "punto partida: {0}".format(pstart)
		aux = random_dir(table_uno, pstart)
		if aux == pstart:
			break
		#print "nos movemos a: {0}".format(table_uno[aux])
		history.append(table_uno[aux])
		pstart = table_uno[aux]
		table_uno.pop(aux)
	
	#print "final: {0}".format(aux)
	return history

def step_one(table_all, table_uno):
	""" Elegir pixel aleatorio del archivo que este libre (no haya camino definido) y sea un numero distinto de cero. """

	print "Paso 1: Generando puzzle:",
	sys.stdout.flush()

	while len(table_uno) > 0:
		ran = random.randint(0, len(table_uno)-1)
		changes = step_two(table_uno, table_uno.pop(ran))
		
		# print ".",
		# sys.stdout.flush()

		for change in changes:
			for x in table_all:
				for y in x:
					for key in y:
						if key == 'posicion':
							if change == y[key]:
								if changes[0] == y[key] or changes[-1] == y[key]:
									y['number'] = len(changes)
									if changes[0] == y[key]:
										y['conn'] = changes
								else:
									y['number'] = -1 # para indicar la solucion correcta
	print "Done"

def write_file(table_all, ncolumns, nrows):
	f = open("temp.csv", 'w')
	for x in xrange(0, nrows):
		for y in xrange(0, ncolumns):
			if table_all[y][x].get('number') == -1:
				f.write('0')
			else:
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
					table_all[y][x] = {'number': 0, 'posicion': (y, x), 'conn': []}
				else:
					table_all[y][x] = {'number': 1, 'posicion': (y, x), 'conn': []}
					table_uno.append((y, x))

	step_one(table_all, table_uno)
	res = cond_dos(table_all)
	print "{0} fallos".format(len(res)/3)
	while len(res) > 0:
		step_one(table_all, res)
		res = cond_dos(table_all)
		print "{0} fallos".format(len(res)/3)

	write_file(table_all, ncolumns, nrows)

	sys.exit()
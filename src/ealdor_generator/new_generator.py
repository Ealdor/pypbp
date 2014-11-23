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
		- Por cada fallo volver al paso 1 (menos el número problemático). Si no hay fallos se ha terminado.
	USE: python new_generator.py <file_path> <maxim> <iters>
		- maxim: max length number (1 - 21).
		- iters: number of iterations per number. High number means more complexity but more time to generate the puzzle (a good value is 10).
	'''

import sys
import pygame
import string
import random

fails = 0
table_uno = None
table_all = None

maxim = 0
iters = 0

i = 0

visited = []

def findfinal(dire, ini, allini):
	global fails

	if (dire[0]+dire[1]) - (allini.get('conn')[-1][0] + allini.get('conn')[-1][1]) > len(allini.get('conn')):
		return False
	elif (allini.get('conn')[-1][0] + allini.get('conn')[-1][1]) - (dire[0]+dire[1]) > len(allini.get('conn')):
		return False
	elif dire[0] >= 0 and dire[1] >= 0 and dire[0] <= ncolumns and dire[1] <= nrows:
		for x in table_all:
			for y in x:
				if y.get('number') == allini.get('number') and y.get('posicion') == dire and y.get('posicion') != ini:
					fails +=1
					if fails == 2:
						return True
	return False

def find(dire, ini, allini):
	if (dire[0]+dire[1]) - (allini.get('conn')[-1][0] + allini.get('conn')[-1][1]) > len(allini.get('conn')):
		return []
	elif (allini.get('conn')[-1][0] + allini.get('conn')[-1][1]) - (dire[0]+dire[1]) > len(allini.get('conn')):
		return []
	elif dire[0] >= 0 and dire[1] >= 0 and dire[0] <= ncolumns and dire[1] <= nrows:
		for x in table_all:
			for y in x:
				if (y.get('number') == 0 or y.get('posicion') in allini.get('conn')) and (y.get('posicion') == dire) and y.get('posicion') != ini and y.get('posicion') != allini.get('conn')[-1] and y.get('posicion') not in visited[0:-1]:
					return [(dire[0], dire[1]-1), (dire[0]+1, dire[1]), (dire[0], dire[1]+1), (dire[0]-1, dire[1])]
	return []

def way_mov(ini, allini):
	global fails, visited
	
	fails = 0

	visited.append(ini)

	# TODO: marcar cada pos de aux con un tercer valor y en find no dejar que vaya en direccion contraria en el return
	aux = [(ini[0], ini[1]-1), (ini[0]+1, ini[1]), (ini[0], ini[1]+1), (ini[0]-1, ini[1])] #up, right, down, left

	# for dire in aux:
	# 	visited.append(dire)
	# 	if allini.get('number') > 2:
	# 		for dire2 in find(dire, ini, allini):
	# 			visited.append(dire2)
	# 			if findfinal(dire2, ini, allini): visited = []; return True
	# 			visited.pop()
	# 	else:
	# 		if findfinal(dire, ini, allini): visited = []; return True
	# 	visited.pop()
	# visited = []

	for dire in aux:
		visited.append(dire)
		if allini.get('number') > 2:
			for dire2 in find(dire, ini, allini):
				visited.append(dire2)
				if allini.get('number') > 3:
					for dire3 in find(dire2, ini, allini):
						visited.append(dire3)
						if allini.get('number') > 4:
							for dire4 in find(dire3, ini, allini):
								visited.append(dire4)
								if allini.get('number') > 5:
									for dire5 in find(dire4, ini, allini):
										visited.append(dire5)
										if allini.get('number') > 6:
											for dire6 in find(dire5, ini, allini):
												visited.append(dire6)
												if allini.get('number') > 7:
													for dire7 in find(dire6, ini, allini):
														visited.append(dire7)
														if allini.get('number') > 8:
															for dire8 in find(dire7, ini, allini):
																visited.append(dire8)
																if allini.get('number') > 9:
																	for dire9 in find(dire8, ini, allini):
																		visited.append(dire9)
																		if allini.get('number') > 10:
																			for dire10 in find(dire9, ini, allini):
																				visited.append(dire10)
																				if allini.get('number') > 11:
																					for dire11 in find(dire10, ini, allini):
																						visited.append(dire11)
																						if allini.get('number') > 12:
																							for dire12 in find(dire11, ini, allini):
																								visited.append(dire12)
																								if allini.get('number') > 13:
																									for dire13 in find(dire12, ini, allini):
																										visited.append(dire13)
																										if allini.get('number') > 14:
																											for dire14 in find(dire13, ini, allini):
																												visited.append(dire14)
																												if allini.get('number') > 15:
																													for dire15 in find(dire14, ini, allini):
																														visited.append(dire15)
																														if allini.get('number') > 16:
																															for dire16 in find(dire15, ini, allini):
																																visited.append(dire16)
																																if allini.get('number') > 17:
																																	for dire17 in find(dire16, ini, allini):
																																		visited.append(dire17)
																																		if allini.get('number') > 18:
																																			for dire18 in find(dire17, ini, allini):
																																				visited.append(dire18)
																																				if allini.get('number') > 19:
																																					for dire19 in find(dire18, ini, allini):
																																						visited.append(dire19)
																																						if allini.get('number') > 20:
																																							for dire20 in find(dire19, ini, allini):
																																								visited.append(dire20)
																																								if findfinal(dire20, ini, allini): visited = []; return True
																																								visited.pop()
																																						else:
																																							if findfinal(dire19, ini, allini): visited = []; return True
																																						visited.pop()
																																				else:
																																					if findfinal(dire18, ini, allini): visited = []; return True
																																				visited.pop()
																																		else:
																																			if findfinal(dire17, ini, allini): visited = []; return True
																																		visited.pop()
																																else:
																																	if findfinal(dire16, ini, allini): visited = []; return True
																																visited.pop()
																														else:
																															if findfinal(dire15, ini, allini): visited = []; return True
																														visited.pop()
																												else:
																													if findfinal(dire14, ini, allini): visited = []; return True
																												visited.pop()
																										else:
																											if findfinal(dire13, ini, allini): visited = []; return True
																										visited.pop()
																								else:
																									if findfinal(dire12, ini, allini): visited = []; return True
																								visited.pop()
																						else:
																							if findfinal(dire11, ini, allini): visited = []; return True
																						visited.pop()
																				else:
																					if findfinal(dire10, ini, allini): visited = []; return True
																				visited.pop()
																		else:
																			if findfinal(dire9, ini, allini): visited = []; return True
																		visited.pop()
																else:
																	if findfinal(dire8, ini, allini): visited = []; return True
																visited.pop()
														else:
															if findfinal(dire7, ini, allini): visited = []; return True
														visited.pop()
												else:
													if findfinal(dire6, ini, allini): visited = []; return True
												visited.pop()
										else:
											if findfinal(dire5, ini, allini): visited = []; return True
										visited.pop()
								else:
									if findfinal(dire4, ini, allini): visited = []; return True
								visited.pop()
						else: 
							if findfinal(dire3, ini, allini): visited = []; return True
						visited.pop()
				else:
					if findfinal(dire2, ini, allini): visited = []; return True
				visited.pop()
		else:
			if findfinal(dire, ini, allini): visited = []; return True
		visited.pop()

	visited = []

	return False

def cond_dos():
	""" COND2: si mediante cuandros blancos o su propio camino hay mas de un camino posible desde un número a su pareja. """

	global table_all, table_uno, maxim, i

	aux = []
	porcent = 0

	for x in table_all:
		for y in x:
			porcent += 1
			print '\rPaso 2: Buscando y corrigiendo posibles fallos: {0}%'.format(porcent/((len(table_all)*len(x))/100)),
			sys.stdout.flush()
			if y.get('number') >= maxim and len(y.get('conn')) > 0:
				if way_mov(y.get('posicion'), y):
					pos = y.get('posicion')
					con = y.get('conn')
					for w in con:
						aux.append(w)
			elif y.get('number') > 0 and y.get('number') < maxim:
				con = y.get('conn')
				for w in con:
					aux.append(w)

	i += 1
	if maxim > 1 and i == iters:
		maxim -= 1
		i = 0

	for w in aux:
		table_all[w[0]][w[1]]['number'] = 1
		table_all[w[0]][w[1]]['conn'] = []

	table_uno = aux

def random_dir(pstart):

	global table_uno

	mov = {'up': None, 'down': None, 'left': None, 'right': None}
	
	try: mov['up'] = table_uno.index((pstart[0], pstart[1]-1))
	except: pass
	try: mov['down'] = table_uno.index((pstart[0], pstart[1]+1))
	except: pass
	try: mov['left'] = table_uno.index((pstart[0]-1, pstart[1]))
	except: pass
	try: mov['right'] = table_uno.index((pstart[0]+1, pstart[1]))
	except: pass	
	
	aux = mov.pop(random.choice(mov.keys()))
	while aux == None and len(mov) > 0:
		aux = mov.pop(random.choice(mov.keys()))
	if aux == None:
		aux = pstart
	return aux

def step_two(pstart):
	""" Elegir aleatoriamente dirección libre y no marcada (no haya sido elegida para este camino antes). """
	
	global table_uno

	history = []
	history.append(pstart)
	
	aux = random_dir(pstart)

	while aux != pstart and len(history) < maxim:
		history.append(table_uno[aux])
		pstart = table_uno[aux]
		table_uno.pop(aux)
		aux = random_dir(pstart)
		if aux == pstart:
			break
	
	return history

def step_one():
	""" Elegir pixel aleatorio del archivo que este libre (no haya camino definido) y sea un numero distinto de cero. """

	global table_all, table_uno

	while len(table_uno) > 0:
		ran = random.randint(0, len(table_uno)-1)
		changes = step_two(table_uno.pop(ran))
		print '\rPaso 1: Generando puzzle: {0}'.format(len(table_uno)),
		sys.stdout.flush()
		
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

	table_all = []
	table_uno = []

	try:
		f = open(sys.argv[1], 'r')
	except IOError:
		print "File not found"
		sys,exit()

	typef = sys.argv[1].split('.')[1]
	maxim = int(sys.argv[2])
	iters = int(sys.argv[3])

	# CONTEO DE COLUMNAS Y FILAS
	if typef == 'csv':
		contador = 0
		ncolumns = len(string.split(string.strip(f.readline()), ','))
		f.seek(0)
		for linea in f.xreadlines( ): contador+= 1
		nrows = contador
		f.seek(0)

	table_all = [[None for y in xrange(0, int(nrows))] for x in xrange(0, int(ncolumns))]

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
	
	while len(table_uno) > 0:
		if maxim == 1:
			break
		step_one()
		print ""
		cond_dos()
		print "- {0} unos (iter: {1}/{2}, number: {3})".format(len(table_uno), i+1, iters, maxim)
		write_file(table_all, ncolumns, nrows)

	write_file(table_all, ncolumns, nrows)

	sys.exit()
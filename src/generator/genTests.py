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
			- Condición 1: si desde un número se llega a uno igual (sin ser pareja) y desde la pareja del último se llega a la pareja del primero. Usando cuadros usados cuyo numero inicial sea igual.
				 4 -1 -1  4
				 4 -1 -1  4
			- Condición 2: si desde un número se llega a uno igual (sin ser pareja) y desde la pareja del último se llega a la pareja del primero. Usando cuadros libres o los de su camino.
				 3  0  3	3 -1
				-1  0 -1    0  3
				 3  0  3
		- Meter los fallos en el listado de unos y volver a generar sobre la lista de unos.
	
	USO: python new_generator.py <file_path> <maxim> <iters>
		- file_path: ruta hacia el archivo csv.
		- maxim: numero maximo que aparecerá en el puzzle (1 - 21 incluido).
		- iters: número de iteraciones por número. Contra mas alto mas complejo será el puzzle resultante pero mas tiempo para la generación:
			- El tiempo de generación depende mucho del numero maximo usado, del tamaño del puzzle y del numero de ceros.
			- Un buen número de iteraciones es entre 1 y 5.

	El archivo resultante es temp.csv (dentro del directorio del generador). '''

''' 1.- Meter en una lista (test) todas las parejas de table_all que cumplan:
	- number > 5
	- c == True
	- distinto de el mismo.

	2.- Por cada elemento de la lista test aplicarle con_dos():
		- funcion find():
			- posicion == dire Y
			- posicion en:
				- sus conexiones O
				- conexiones del otro
		- funcion findfinal():
			- posicion == dire Y 
			- posicion en:
				- ultimo elemento de sus conexiones -> fail + 1
				- ultimo elemento de las conexiones del otro -> fail + 1
				- si fail == 2 -> aplicarle con_dos() al otro:
					- si fail del otro == 2 -> existe un fallo '''

import sys
import pygame
import string
import random
import math
import time
import pickle

fails = 0
table_uno = None
table_all = None

maxim = 0
iters = 0

i = 0

visited = []
destiny = None

lc = True
llc = True
lllc = True

def euclide(dire, dire2):
	return abs( int(round(math.sqrt( (dire[0] - dire2[0])**2 + (dire[1] - dire2[1])**2 ))))

def findfinal(dire, ini, allini):
	global fails

	if dire[0] >= -1 and dire[1] >= -1 and dire[0] <= ncolumns+1 and dire[1] <= nrows+1:
		for x in table_all:
			for y in x:
				if lc or llc: # condición 1 y 2
					if y.get('posicion') == dire and y.get('number') == allini.get('number') and y.get('posicion') not in visited[0:-1]:
						# si el fallo es debido a llegar a uno que no es su pareja original
						if y.get('posicion') != allini.get('conn')[-1]:
							if y.get('c') == True:
								if euclide(y.get('conn')[-1], allini.get('conn')[-1]) >= len(allini.get('conn')):
									fails += 0
								else:
									fails += 1
							else:
								if len(y.get('conn')) > 0 and euclide(y.get('conn')[0], allini.get('conn')[-1]) >= len(allini.get('conn')):
									fails += 0
								else:
									fails += 1
						elif y.get('posicion') == allini.get('conn')[-1]:
							fails += 1

						if fails == 2:
							return True
				elif lllc:
					if dire == y.get('posicion'):
						if y.get('posicion') == allini.get('conn')[-1]:
							fails += 1
						if fails == 2:
							return True
	return False

def find(dire, ini, allini):
	if dire[0] >= -1 and dire[1] >= -1 and dire[0] <= ncolumns+1 and dire[1] <= nrows+1:
		for x in table_all:
			for y in x:
				if lc: # condición 1
					if y.get('posicion') == dire and y.get('number') == -1 and y.get('ps') == allini.get('ps') and y.get('posicion') != ini and y.get('posicion') != allini.get('conn')[-1] and y.get('posicion') not in visited[0:-1]:
						return [(dire[0], dire[1]-1), (dire[0]+1, dire[1]), (dire[0], dire[1]+1), (dire[0]-1, dire[1])]	
				elif llc: # condición 2
					if y.get('posicion') == dire and (y.get('number') == 0 or y.get('posicion') in allini.get('conn')) and y.get('posicion') != ini and y.get('posicion') != allini.get('conn')[-1] and y.get('posicion') not in visited[0:-1]:
						return [(dire[0], dire[1]-1), (dire[0]+1, dire[1]), (dire[0], dire[1]+1), (dire[0]-1, dire[1])]
				elif lllc:
					if dire == y.get('posicion') and (y.get('posicion') in allini.get('conn') or y.get('posicion') in destiny.get('conn')) and y.get('posicion') not in visited[0:-1] and y.get('posicion') != allini.get('conn')[-1] and y.get('posicion') != destiny.get('conn')[-1]:
						return [(dire[0], dire[1]-1), (dire[0]+1, dire[1]), (dire[0], dire[1]+1), (dire[0]-1, dire[1])]	
	return []

def way_mov(ini, allini):
	global fails, visited
	
	fails = 0

	visited.append(ini)

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
			if findfinal(dire, ini, allini): 
				visited = []; return True
		visited.pop()

	visited = []

	return False

def cond_dos():
	""" COND2: si mediante cuandros blancos o su propio camino hay mas de un camino posible desde un número a su pareja. """

	global table_all, destiny

	porcent = 0

	if lllc:
		table_aux = []
		for x in table_all:
			for y in x:
				porcent += 1
				print "\rBuscando y corrigiendo posibles fallos (condición 3): {0}%".format(porcent/((len(table_all)*len(x))/100)),
				sys.stdout.flush()
				if y.get('number') >= 6 and y.get('c') == True:
					for w in table_all:
						for z in w:
							if y != z and z.get('number') >= 6 and z.get('c') == True and ((y,z) not in table_aux and (z,y) not in table_aux):
								table_aux.append((y,z))

		porcent = 0
		for x in table_aux:
			porcent += 1
			print "\rBuscando y corrigiendo posibles fallos (condición 3): {0}/{1}".format(porcent,len(table_aux)),
			sys.stdout.flush()
			if len(x[0].get('conn')) > 0 and len(x[1].get('conn')) > 0:
				destiny = x[1]
				if way_mov(x[0].get('posicion'), x[0]):
					destiny = x[0]
					if way_mov(x[1].get('posicion'), x[1]):
						# print "FAIL"
						if x[0].get('number') > x[1].get('number'):
							con = x[1].get('conn')
						else:
							con = x[0].get('conn')
						for w in con:
							table_all[w[0]][w[1]]['number'] = 1
							table_all[w[0]][w[1]]['conn'] = []
							table_all[w[0]][w[1]]['c'] = False
							table_all[w[0]][w[1]]['ps'] = 1

	else:
		for x in table_all:
			for y in x:
				porcent += 1
				if lc:
					try: print '\rBuscando y corrigiendo posibles fallos (condición 1): {0}%'.format(porcent/((len(table_all)*len(x))/100)),
					except: print '\rBuscando y corrigiendo posibles fallos (condición 1): 100%'
				elif llc:
					try: print '\rBuscando y corrigiendo posibles fallos (condición 2): {0}%'.format(porcent/((len(table_all)*len(x))/100)),
					except: print '\rBuscando y corrigiendo posibles fallos (condición 2): 100%'
				sys.stdout.flush()
				if len(y.get('conn')) >= maxim and y.get('c') == True:
					if way_mov(y.get('posicion'), y):
						con = y.get('conn')
						for w in con:
							table_all[w[0]][w[1]]['number'] = 1
							table_all[w[0]][w[1]]['conn'] = []
							table_all[w[0]][w[1]]['c'] = False
							table_all[w[0]][w[1]]['ps'] = 1
				elif y.get('number') > 0 and y.get('number') < maxim:
					con = y.get('conn')
					for w in con:
						table_all[w[0]][w[1]]['number'] = 1
						table_all[w[0]][w[1]]['conn'] = []
						table_all[w[0]][w[1]]['c'] = False
						table_all[w[0]][w[1]]['ps'] = 1

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
		# changes = step_two(table_uno.pop())
		print '\rGenerando puzzle: {0}'.format(len(table_uno)),
		sys.stdout.flush()
		
		for change in changes:
			for x in table_all:
				for y in x:
					if y['posicion'] == change:
						if changes[0] == y['posicion'] or changes[-1] == y['posicion']:
							y['number'] = len(changes)
							y['conn'] = changes
							if changes[0] == y['posicion']:
								y['c'] = True

						else:
							y['number'] = -1 # para indicar la solucion correcta
							y['c'] = False
							y['conn'] = []
						y['ps'] = len(changes)

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

	with open("temp.pickle", 'wb') as f:
		pickle.dump(table_all, f)

	with open("temp.pickle", 'rb') as f:
		t = pickle.load(f)

def count_one():
	global table_uno

	table_uno = []

	j = 0
	for x in table_all:
		for y in x:
			if y.get('number') == 1:
				j+= 1
				table_uno.append(y.get('posicion'))
	return j

if __name__ == "__main__":

	start_time = time.time()

	table_all = []
	table_uno = []

	try:
		f = open(sys.argv[1], 'r')
	except IOError:
		print "File not found"
		sys.exit()

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
					table_all[y][x] = {'number': 0, 'posicion': (y, x), 'conn': [], 'ps': 0}
				elif tn == 1:
					table_all[y][x] = {'number': 1, 'posicion': (y, x), 'conn': [], 'ps': 1, 'c': False}
					table_uno.append((y, x))
	
	print "== Generando puzzle y asegurando solución única =="
	while True:
		if maxim == 1:
			break

		i += 1

		step_one()
		
		lc = True
		llc = False
		lllc = False
		cond_dos()
		# usando -unos o posiciones cuyo inicio sea del mismo numero conseguir llegar a un numero que no sea su pareja original y que sea posible conectar ambas parejas
		# print "- \r{0} unos (iter: {1}/{2}, number: {3}) - {4} seg".format(count_one(), i, iters, maxim, int(time.time() - start_time)),

		lc = False
		llc = True
		lllc = False
		cond_dos()
		# usando ceros o posiciones de su camino llegar a un numero que no sea su pareja original y que sea posible conectar ambas parejas 
		# print "- \r{0} unos (iter: {1}/{2}, number: {3}) - {4} seg".format(count_one(), i, iters, maxim, int(time.time() - start_time)),

		lc = False
		llc = False
		lllc = True
		cond_dos()
		# usando ceros o posiciones de su camino llegar a un numero que no sea su pareja original y que sea posible conectar ambas parejas 
		print "- {0} unos (iter: {1}/{2}, number: {3}) - {4} seg".format(count_one(), i, iters, maxim, int(time.time() - start_time))

		if i == iters:
			maxim -= 1
			i = 0

	print "== Resumen =="
	print "Total de unos: {0} - Tiempo: {1} seg".format(count_one(), int(time.time() - start_time))

	write_file(table_all, ncolumns, nrows)

	sys.exit()
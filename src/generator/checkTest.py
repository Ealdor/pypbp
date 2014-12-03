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

table_all = None

visited = []

lc = False

destiny = None

def findfinal(dire, ini, allini):
	global fails

	if True:
		for x in table_all:
			for y in x:
				if dire == y.get('posicion'):
					if y.get('posicion') == allini.get('conn')[-1]:
						fails += 1
					if fails == 2:
						return True
				
	return False

def find(dire, ini, allini):
	if True:
		for x in table_all:
			for y in x:
				if dire == y.get('posicion') and (y.get('posicion') in allini.get('conn') or y.get('posicion') in destiny.get('conn')) and y.get('posicion') not in visited[0:-1] and y.get('posicion') != allini.get('conn')[-1] and y.get('posicion') != destiny.get('conn')[-1]:
					return [(dire[0], dire[1]-1), (dire[0]+1, dire[1]), (dire[0], dire[1]+1), (dire[0]-1, dire[1])]	

	return []

def way_mov(ini, allinii):
	global fails, visited, destiny
	
	fails = 0

	if not lc:
		destiny = allinii[1]
		allini = allinii[0]
	else:
		destiny = allinii[0]
		allini = allinii[1]

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

	global table_all, lc

	table_uno = []
	porcent = 0

	for x in table_all:
		for y in x:
			if y.get('number') >= 6 and y.get('c') == True:
				for w in table_all:
					for z in w:
						if y != z and z.get('number') >= 6 and z.get('c') == True and ((y,z) not in table_uno and (z,y) not in table_uno):
							table_uno.append((y,z))

	for x in table_uno:
		porcent += 1
		print "\r{0} / {1}".format(porcent, len(table_uno)),
		if len(x[0].get('conn')) > 0 and len(x[1].get('conn')) > 0:
			lc = False
			if way_mov(x[0].get('posicion'), x):
				lc = True
				if way_mov(x[1].get('posicion'), x):
					print "\nFAIL entre {0}{2} y {1}{3}".format(x[0].get('number'), x[1].get('number'), x[0].get('posicion'), x[1].get('posicion'))
					# print "FAIL"
					if x[0].get('number') > x[1].get('number'):
						con = x[1].get('conn')
					else:
						con = x[0].get('conn')
					for w in con:
						table_all[w[0]][w[1]]['number'] = -2
						table_all[w[0]][w[1]]['conn'] = []
						table_all[w[0]][w[1]]['c'] = False
						table_all[w[0]][w[1]]['ps'] = 1

def write_file(table_all, ncolumns, nrows):
	f = open("temp_fix.csv", 'w')
	for x in xrange(0, nrows):
		for y in xrange(0, ncolumns):
			if table_all[y][x].get('number') == -1:
				f.write('0')
			else:
				f.write(str(table_all[y][x].get('number')))
			if y == ncolumns-1: f.write('\n')
			else: f.write(',')

if __name__ == "__main__":

	start_time = time.time()

	table_all = []

	try:
		f = open(sys.argv[1], 'r')
	except IOError:
		print "File not found"
		sys.exit()

	with open("temp.pickle", 'rb') as f:
		table_all = pickle.load(f)
	
	cond_dos()

	write_file(table_all, 42, 50)

	sys.exit()
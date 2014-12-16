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
		- Meter los fallos en el listado de unos y volver a generar sobre la lista de unos. '''

''' Condicion 3:
	1.- Meter en una lista (test) todas las parejas de table_all que cumplan:
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
import string
import random
import math
import time
import pickle
import utils

class Generator():
	def __init__(self, maxim, iters, table_all, button, typ):
		self.table_all = table_all
		self.maxim = int(maxim)
		self.iters = int(iters)

		self.table_uno = {}
		self.fails = 0
		self.visited = []
		self.destiny = None
		self.types = 0

		self.typ = typ
		self.cancel = False
		self.button = button

	def findfinal(self, dire, ini, allini):
		if dire[0] >= 0 and dire[1] >= 0 and dire[0] <= utils.ncolumns and dire[1] <= utils.nrows:
			for x in self.table_all:
				for y in x:
					if self.types == 1 or self.types == 2: # condición 1 y 2
						if y.get('posicion') == dire and y.get('number') == allini.get('number') and y.get('posicion') not in self.visited[0:-1]:
							# si el fallo es debido a llegar a uno que no es su pareja original
							if y.get('posicion') != allini.get('conn')[-1] and y.get('color') == allini.get('color'):
								if y.get('c') == True:
									if utils.euclide(y.get('conn')[-1], allini.get('conn')[-1]) >= len(allini.get('conn')):
										self.fails += 0
									else:
										self.fails += 1
								else:
									if len(y.get('conn')) > 0 and utils.euclide(y.get('conn')[0], allini.get('conn')[-1]) >= len(allini.get('conn')):
										self.fails += 0
									else:
										self.fails += 1
							elif y.get('posicion') == allini.get('conn')[-1]:
								self.fails += 1

							if self.fails == 2:
								return True
					elif self.types == 3:
						if dire == y.get('posicion'):
							if y.get('posicion') == allini.get('conn')[-1]:
								self.fails += 1
							if self.fails == 2:
								return True
		return False

	def find(self, dire, ini, allini):
		self.button.update()
		if self.cancel:
			return []
		if dire[0] >= 0 and dire[1] >= 0 and dire[0] <= utils.ncolumns and dire[1] <= utils.nrows:
			for x in self.table_all:
				for y in x:
					if self.types == 1: # condición 1
						if y.get('posicion') == dire and y.get('color') == allini.get('color') and y.get('number') == -1 and y.get('ps') == allini.get('ps') and y.get('posicion') != ini and y.get('posicion') != allini.get('conn')[-1] and y.get('posicion') not in self.visited[0:-1]:
							return [(dire[0], dire[1]-1), (dire[0]+1, dire[1]), (dire[0], dire[1]+1), (dire[0]-1, dire[1])]	
					elif self.types == 2: # condición 2
						if y.get('posicion') == dire and (y.get('number') == 0 or y.get('posicion') in allini.get('conn')) and y.get('posicion') != ini and y.get('posicion') != allini.get('conn')[-1] and y.get('posicion') not in self.visited[0:-1]:
							if utils.euclide(y.get('posicion'), allini.get('conn')[-1]) >= len(allini.get('conn')):
								return []
							else:
								return [(dire[0], dire[1]-1), (dire[0]+1, dire[1]), (dire[0], dire[1]+1), (dire[0]-1, dire[1])]
					elif self.types == 3:
						# and y.get('color') == allini.get('color')
						if dire == y.get('posicion') and (y.get('posicion') in allini.get('conn') or y.get('posicion') in self.destiny.get('conn') or y.get('number') == 0) and y.get('posicion') not in self.visited[0:-1] and y.get('posicion') != allini.get('conn')[-1] and y.get('posicion') != self.destiny.get('conn')[-1] and y.get('posicion') != self.destiny.get('conn')[0]:
							if utils.euclide(y.get('posicion'), allini.get('conn')[-1]) >= len(allini.get('conn')):
								return []
							else:
								return [(dire[0], dire[1]-1), (dire[0]+1, dire[1]), (dire[0], dire[1]+1), (dire[0]-1, dire[1])]	
		return []

	def way_mov(self, ini, allini):
		self.button.update()
		if self.cancel:
			return False

		self.fails = 0
		self.visited.append(ini)
		aux = [(ini[0], ini[1]-1), (ini[0]+1, ini[1]), (ini[0], ini[1]+1), (ini[0]-1, ini[1])] #up, right, down, left

		for dire in aux:
			self.visited.append(dire)
			if allini.get('number') > 2:
				for dire2 in self.find(dire, ini, allini):
					self.visited.append(dire2)
					if allini.get('number') > 3:
						for dire3 in self.find(dire2, ini, allini):
							self.visited.append(dire3)
							if allini.get('number') > 4:
								for dire4 in self.find(dire3, ini, allini):
									self.visited.append(dire4)
									if allini.get('number') > 5:
										for dire5 in self.find(dire4, ini, allini):
											self.visited.append(dire5)
											if allini.get('number') > 6:
												for dire6 in self.find(dire5, ini, allini):
													self.visited.append(dire6)
													if allini.get('number') > 7:
														for dire7 in self.find(dire6, ini, allini):
															self.visited.append(dire7)
															if allini.get('number') > 8:
																for dire8 in self.find(dire7, ini, allini):
																	self.visited.append(dire8)
																	if allini.get('number') > 9:
																		for dire9 in self.find(dire8, ini, allini):
																			self.visited.append(dire9)
																			if allini.get('number') > 10:
																				for dire10 in self.find(dire9, ini, allini):
																					self.visited.append(dire10)
																					if allini.get('number') > 11:
																						for dire11 in self.find(dire10, ini, allini):
																							self.visited.append(dire11)
																							if allini.get('number') > 12:
																								for dire12 in self.find(dire11, ini, allini):
																									self.visited.append(dire12)
																									if allini.get('number') > 13:
																										for dire13 in self.find(dire12, ini, allini):
																											self.visited.append(dire13)
																											if allini.get('number') > 14:
																												for dire14 in self.find(dire13, ini, allini):
																													self.visited.append(dire14)
																													if allini.get('number') > 15:
																														for dire15 in self.find(dire14, ini, allini):
																															self.visited.append(dire15)
																															if allini.get('number') > 16:
																																for dire16 in self.find(dire15, ini, allini):
																																	self.visited.append(dire16)
																																	if allini.get('number') > 17:
																																		for dire17 in self.find(dire16, ini, allini):
																																			self.visited.append(dire17)
																																			if allini.get('number') > 18:
																																				for dire18 in self.find(dire17, ini, allini):
																																					self.visited.append(dire18)
																																					if allini.get('number') > 19:
																																						for dire19 in self.find(dire18, ini, allini):
																																							self.visited.append(dire19)
																																							if allini.get('number') > 20:
																																								for dire20 in self.find(dire19, ini, allini):
																																									self.visited.append(dire20)
																																									if self.findfinal(dire20, ini, allini): self.visited = []; return True
																																									self.visited.pop()
																																							else:
																																								if self.findfinal(dire19, ini, allini): self.visited = []; return True
																																							self.visited.pop()
																																					else:
																																						if self.findfinal(dire18, ini, allini): self.visited = []; return True
																																					self.visited.pop()
																																			else:
																																				if self.findfinal(dire17, ini, allini): self.visited = []; return True
																																			self.visited.pop()
																																	else:
																																		if self.findfinal(dire16, ini, allini): self.visited = []; return True
																																	self.visited.pop()
																															else:
																																if self.findfinal(dire15, ini, allini): self.visited = []; return True
																															self.visited.pop()
																													else:
																														if self.findfinal(dire14, ini, allini): self.visited = []; return True
																													self.visited.pop()
																											else:
																												if self.findfinal(dire13, ini, allini): self.visited = []; return True
																											self.visited.pop()
																									else:
																										if self.findfinal(dire12, ini, allini): self.visited = []; return True
																									self.visited.pop()
																							else:
																								if self.findfinal(dire11, ini, allini): self.visited = []; return True
																							self.visited.pop()
																					else:
																						if self.findfinal(dire10, ini, allini): self.visited = []; return True
																					self.visited.pop()
																			else:
																				if self.findfinal(dire9, ini, allini): self.visited = []; return True
																			self.visited.pop()
																	else:
																		if self.findfinal(dire8, ini, allini): self.visited = []; return True
																	self.visited.pop()
															else:
																if self.findfinal(dire7, ini, allini): self.visited = []; return True
															self.visited.pop()
													else:
														if self.findfinal(dire6, ini, allini): self.visited = []; return True
													self.visited.pop()
											else:
												if self.findfinal(dire5, ini, allini): self.visited = []; return True
											self.visited.pop()
									else:
										if self.findfinal(dire4, ini, allini): self.visited = []; return True
									self.visited.pop()
							else: 
								if self.findfinal(dire3, ini, allini): self.visited = []; return True
							self.visited.pop()
					else:
						if self.findfinal(dire2, ini, allini): self.visited = []; return True
					self.visited.pop()
			else:
				if self.findfinal(dire, ini, allini): self.visited = []; return True
			self.visited.pop()

		self.visited = []

		return False

	def cond_dos(self, types):
		""" COND2: si mediante cuandros blancos o su propio camino hay mas de un camino posible desde un número a su pareja. """
		self.types = types
		porcent = 0

		if self.types == 3:
			table_aux = []
			for x in self.table_all:
				for y in x:
					self.button.update()
					porcent += 1
					self.typ.set("Progreso: {0}/{1} (1º etapa)".format(porcent, len(self.table_all)*len(x)))
					if y.get('number') >= 4 and y.get('c') == True:
						for w in self.table_all:
							for z in w:
								if y != z and z.get('number') >= 4 and z.get('number') <= self.maxim and z.get('c') == True and ((y,z) not in table_aux and (z,y) not in table_aux):
									if y.get('number') > z.get('number'):
										for pun in y.get('conn'):
											if utils.euclide(pun, z.get('posicion')) <= len(z.get('conn')):
												table_aux.append((y,z))
												break
									else:
										for pun in z.get('conn'):
											if utils.euclide(pun, y.get('posicion')) <= len(y.get('conn')):
												table_aux.append((y,z))
												break

			porcent = 0
			for x in table_aux:
				self.button.update()
				porcent += 1
				self.typ.set("Progreso: {0}/{1} (2º etapa)".format(porcent, len(table_aux)))
				if len(x[0].get('conn')) > 0 and len(x[1].get('conn')) > 0:
					self.destiny = x[1]
					if self.way_mov(x[0].get('posicion'), x[0]):
						self.destiny = x[0]
						if self.way_mov(x[1].get('posicion'), x[1]):
							if x[0].get('number') > x[1].get('number'):
								con = x[1].get('conn')
							else:
								con = x[0].get('conn')
							# con = x[0].get('conn')
							# for w in con:
							# 	self.table_all[w[0]][w[1]]['number'] = 1
							# 	self.table_all[w[0]][w[1]]['conn'] = []
							# 	self.table_all[w[0]][w[1]]['c'] = False
							# 	self.table_all[w[0]][w[1]]['ps'] = 1
							# con = x[1].get('conn')
							for w in con:
								self.table_all[w[0]][w[1]]['number'] = 1
								self.table_all[w[0]][w[1]]['conn'] = []
								self.table_all[w[0]][w[1]]['c'] = False
								self.table_all[w[0]][w[1]]['ps'] = 1

		else:
			for x in self.table_all:
				for y in x:
					porcent += 1
					self.typ.set("Progreso: {0}/{1}".format(porcent, len(self.table_all)*len(x)))
					if len(y.get('conn')) >= self.maxim and y.get('c') == True:

						if (self.types == 2 and y.get('number') == self.maxim) or self.types == 1:

							if self.way_mov(y.get('posicion'), y):
								con = y.get('conn')
								for w in con:
									self.table_all[w[0]][w[1]]['number'] = 1
									self.table_all[w[0]][w[1]]['conn'] = []
									self.table_all[w[0]][w[1]]['c'] = False
									self.table_all[w[0]][w[1]]['ps'] = 1
					elif y.get('number') > 0 and y.get('number') < self.maxim:
						con = y.get('conn')
						for w in con:
							self.table_all[w[0]][w[1]]['number'] = 1
							self.table_all[w[0]][w[1]]['conn'] = []
							self.table_all[w[0]][w[1]]['c'] = False
							self.table_all[w[0]][w[1]]['ps'] = 1

	def random_dir(self, pstart, cstart):
		mov = {'up': None, 'down': None, 'left': None, 'right': None}
		
		if self.table_uno.get((pstart[0], pstart[1]-1)) == cstart:
			mov['up'] = (pstart[0], pstart[1]-1)
		if self.table_uno.get((pstart[0], pstart[1]+1)) == cstart:
			mov['down'] = (pstart[0], pstart[1]+1)
		if self.table_uno.get((pstart[0]-1, pstart[1])) == cstart:
			mov['left'] = (pstart[0]-1, pstart[1])
		if self.table_uno.get((pstart[0]+1, pstart[1])) == cstart:
			mov['right'] = (pstart[0]+1, pstart[1])	
		
		aux = mov.pop(random.choice(mov.keys()))
		while aux == None and len(mov) > 0:
			aux = mov.pop(random.choice(mov.keys()))
		if aux == None:
			aux = pstart
		return aux

	def step_two(self, pstart, cstart):
		""" Elegir aleatoriamente dirección libre y no marcada (no haya sido elegida para este camino antes). """
		
		history = []
		history.append(pstart)
		
		aux = self.random_dir(pstart, cstart)

		while aux != pstart and len(history) < self.maxim:
			history.append(aux)
			pstart = aux
			self.table_uno.pop(aux)
			aux = self.random_dir(pstart, cstart)
			if aux == pstart:
				break
		
		return history

	def step_one(self):
		""" Elegir pixel aleatorio del archivo que este libre (no haya camino definido) y sea un numero distinto de cero. """

		while len(self.table_uno) > 0:
			self.button.update()
			if self.cancel:
				break
			self.typ.set("Progreso: {0}".format(len(self.table_uno)))
			ran = random.choice(self.table_uno.keys())
			changes = self.step_two(ran, self.table_uno.pop(ran))
			# changes = self.step_two(table_uno.pop())
			
			for change in changes:
				for x in self.table_all:
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

	def count_one(self):
		self.table_uno = {}
		for x in self.table_all:
			for y in x:
				if y.get('number') == 1:
					self.table_uno[y.get('posicion')] = y.get('color')

if __name__ == "__main__":
	sys.exit()
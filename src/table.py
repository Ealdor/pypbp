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

import sys
import pygame
import pygame.locals
from constants import *
from cells import *

class Table():
	""" Clase que representa un tablero

    Args:
        twidth(int): altura
        theight(int): anchura
        tposx(int): posición horizontal
        tposy(int): posición vertical
        table(list): puzzle

    Attributes:
    	tsurface(Surface): superficie del tablero
    	table(list): lista de celdas
    	cellsprite(CellSprite): sprite seleccionador
    	sprites_list(list): lista para guardar el sprite seleccionador
    	nfont(Font): fuente
    	history(list): lista para guardar la historia de movimiento
    	stop(bool): atributo para parar 
    	tcheck(int): variable de comprobacion de puzzle completo
    	
    """	

	def __init__(self, twidth, theight, tposx, tposy, table, screen):
		self.twidth = twidth
		self.theight = theight
		self.tposx = tposx
		self.tposy = tposy
		self.tsurface = pygame.Surface([self.twidth*CELL_WIDTH, self.theight*CELL_WIDTH])
		self.tsurface_aux = None
		self.old = None
		self.oldcon = []
		self.oldhist = []
		self.dim = self.tsurface.get_size()
		self.table = table
		self.cellsprite = CellSprite(self.table[0][0], 3)
		self.sprites_list = pygame.sprite.Group()
		self.sprites_list.add(self.cellsprite)
		self.nfont = pygame.font.SysFont(None, FONT_SIZE)
		self.history = []
		self.stop = False
		self.tcheck = 0
		self.screen = screen
		self.zoom = self.dim
		self.win()
		self.first_draw()

	def first_draw(self):
		""" Función que dibuja todo el tablero completo """

		self.tsurface.fill(WHITE)
		for x in xrange(0, self.twidth):
			for y in xrange(0, self.theight):
				cell = self.table[x][y]
				if cell.background_color != WHITE: # dibujamos el fondo de la celda si es distinto de blanco
					pygame.draw.rect(self.tsurface, cell.background_color, cell.rect, 0)
				pygame.draw.rect(self.tsurface, cell.border_color, cell.rect, cell.bsize) # dibujamos el borde de la celda
				if cell.number != 0: # dibujamos el número de la celda si no es cero
					self.tsurface.blit(self.nfont.render(str(cell.number), True, cell.number_color, cell.background_color), (cell.posx+(CELL_WIDTH - self.nfont.size(str(cell.number))[0])/2, cell.posy+(CELL_WIDTH - self.nfont.size(str(cell.number))[1])/2))
		self.tsurface_aux = self.tsurface.copy()
		self.old = self.cellsprite.cell # guardamos el anterior

	def win(self):
		""" Función que define la regla para superar el puzzle """

		for x in self.table:
			for cell in x:
				if cell.number > 1:
					self.tcheck += cell.number
				elif cell.number == 1:
					self.tcheck += cell.number+1

	def update(self, lista):
		""" Función que actualiza en la pantalla una celda o lista de celdas """

		for x in lista:
			if (x.number == 0 and len(x.lines) > 1 and x.background_color == WHITE) or (x.number != 0 and len(x.lines) > 1 and x.background_color == WHITE and x.number_color != GREY) or (x.number == 1 and len(x.lines) > 1): # limpieza por errores
				x.lines = x.lines[0:1]
			pygame.draw.rect(self.tsurface, x.background_color, x.rect, 0)
			pygame.draw.rect(self.tsurface, x.border_color, x.rect, x.bsize)
			if len(x.lines) > 1: # dibujamos las lineas de conexión de la celda si hay
				pygame.draw.lines(self.tsurface, x.lines_color, False, x.lines, x.lsize)
			if x.number != 0:
				self.tsurface.blit(self.nfont.render(str(x.number), True, x.number_color, x.background_color), (x.posx+(CELL_WIDTH - self.nfont.size(str(x.number))[0])/2, x.posy+(CELL_WIDTH - self.nfont.size(str(x.number))[1])/2))

	def draw(self):
		""" Función para dibujar el tablero y todos sus componenetes (cell y cellsprite) """

		# CONTROLAMOS LA CAMARA
		sd = self.screen.get_size()
		camd = (sd[0]/CELL_WIDTH) / 2, (sd[1]/CELL_WIDTH) / 2
		aux = [0, 0, sd[0], sd[1]] # solo actualizamos la parte de la pantalla que se ve (FPS!!!1!11!!)
		if self.cellsprite.cell.posx/CELL_WIDTH >= camd[0]-1:
			aux[0] = (((self.cellsprite.cell.posx/CELL_WIDTH)-camd[0])*CELL_WIDTH)+(2*CELL_WIDTH)
		if self.cellsprite.cell.posy/CELL_WIDTH >= camd[1]-1:
			aux[1] = (((self.cellsprite.cell.posy/CELL_WIDTH)-camd[1])*CELL_WIDTH)+(2*CELL_WIDTH)

		# DIBUJAMOS
		self.screen.fill(FONDO)
		self.tsurface_aux = self.tsurface.copy() # bliteamos una copia de la anterior
		self.screen.blit(self.tsurface_aux, (self.tposx*CELL_WIDTH, self.tposy*CELL_WIDTH), (aux[0], aux[1], sd[0]-2*CELL_WIDTH-4, sd[1]-2*CELL_WIDTH))
		self.update([self.old]) # ANTERIOR
		self.update([self.cellsprite.cell]) # ACTUAL
		self.update(self.cellsprite.cell.connections) # CONEXIONES (levantamos y correcto)
		self.update(self.oldcon) # CONEXIONES (levantamos y no correcto)
		if len(self.oldcon) > 0: self.oldcon = []
		self.update(self.oldhist) # HISTORIA (en proceso)
		if len(self.oldhist) > 0: self.oldhist = []
		self.sprites_list.draw(self.tsurface) # dibujamos el cellsprite
		self.screen.blit(self.tsurface, (self.tposx*CELL_WIDTH, self.tposy*CELL_WIDTH), (aux[0], aux[1], sd[0]-2*CELL_WIDTH-4, sd[1]-2*CELL_WIDTH))
		self.old = self.cellsprite.cell # guardamos el anterior
		
		# ZOOM
		if self.zoom != self.dim: 
			self.screen.fill(FONDO)
			self.screen.blit(pygame.transform.scale(self.tsurface, self.zoom), (self.tposx*CELL_WIDTH, self.tposy*CELL_WIDTH), aux)
		
		# INTERFAZ
		if self.tcheck == 0: self.screen.blit(self.nfont.render("WELL DONE!", True, BLUE, FONDO), (CELL_WIDTH, 3)) # MARCADOR
		else:
			self.screen.blit(self.nfont.render("Pixel: {0}, {1}".format(self.cellsprite.cell.number, self.cellsprite.cell.color), True, BLACK, FONDO), (CELL_WIDTH, 3))
			self.screen.blit(self.nfont.render("{0} LEFT".format(self.tcheck), True, RED, FONDO), (CELL_WIDTH*9, 3))

	def check(self, event):
		""" Función para recoger los eventos del teclado 

		Attributes:
			event(Event): evento de pygame

		Returns:
			bool(bool): True si hay movimiento o pulsación

		"""

		amm = 1
		if pygame.key.get_pressed()[pygame.locals.K_x] != 0: # presionada la x
			amm = 5
		if event.type == pygame.locals.KEYDOWN:
			if pygame.key.get_pressed()[pygame.locals.K_SPACE] != 0: # presionamos el espacio
				if event.key == pygame.locals.K_DOWN:
					self.process(1, True, (0, 1))
				elif event.key == pygame.locals.K_UP:
					self.process(2, True, (0, -1))
				elif event.key == pygame.locals.K_LEFT:
					self.process(3, True, (-1, 0))
				elif event.key == pygame.locals.K_RIGHT:
					self.process(4, True, (1, 0))
				elif event.key == pygame.locals.K_SPACE:
					self.process(0, True)
			elif event.key == pygame.locals.K_DOWN:
				self.process(1, False, (0, amm))
			elif event.key == pygame.locals.K_UP:
				self.process(2, False, (0, -amm))
			elif event.key == pygame.locals.K_LEFT:
				self.process(3, False, (-amm, 0))
			elif event.key == pygame.locals.K_RIGHT:
				self.process(4, False, (amm, 0))
			elif event.key == pygame.locals.K_c: # c (borrar)
				self.process(6, False)
			elif event.unicode == '-': # zoom out
				aux = (self.zoom[0]-self.twidth, self.zoom[1]-self.theight)
				if aux[0] > 0 and aux[1] > 0:
					self.cell_move(self.table[0][0])
					self.zoom = aux
			elif event.unicode == '+': # restore zoom
				self.zoom = self.dim
				self.stop = False
			return True
		elif event.type == pygame.locals.KEYUP and event.key == pygame.locals.K_SPACE: # levantamos el espacio
			self.process(5, False)
			return True
		else:
			return False

	def cell_draw(self, cell, color):
		""" Función para poner colores de dibujo

		Attributes:
			cell(Cell): celda a dibujar
			color(Color): el color del numero de la celda

		"""

		cell.background_color = color
		cell.number_color = WHITE

	def cell_clear(self, cell):
		""" Función para poner colores de borrado

		Attributes:
			cell(Cell): celda a borrar

		"""

		cell.background_color = WHITE
		cell.number_color = cell.color

	def cell_move(self, cell):
		""" Función para mover la celda

		Attributes:
			cell(Cell): celda a mover

		"""

		self.cellsprite.cell = cell
		self.cellsprite.rect = cell.rect

	def process(self, types, space, mov = (0, 0)):
		""" Función para procesar los eventos del teclado. Las reglas del juego.

		Attributes:
			types(int): tipo de tecla
			space(bool): espacio presionado o no
			mov(set): cuanto nos movemos

		"""

		if (self.zoom == self.dim):
			oldCell = self.cellsprite.cell
			if types == 0: # presionamos del espacio
				# reglas para INICIAR
				if oldCell.number != 0 and len(oldCell.connections) == 0:
					self.history.append(oldCell)
					self.cell_draw(oldCell, oldCell.color)
				else:
					self.stop = True
			elif types == 5: # levantamos el espacio
				# reglas para SOLTAR
				if len(self.history) > 0 and len(self.history) == oldCell.number and self.history[0].number == oldCell.number and oldCell.number_color != GREY:
					for cell in self.history: # dibujamos
						cell.connections = self.history
						if cell.number_color == GREY:
							cell.number = 0
						self.cell_draw(cell, self.history[0].color)
					self.tcheck -= self.history[0].number + self.history[-1].number
				else: # si no se cumplen las reglas
					self.oldhist = self.history
					for cell in self.history: # limpiamos
						cell.lines = cell.lines[:1]
						if cell.number_color == GREY:
							cell.number = 0
						self.cell_clear(cell)
				self.history = []
				self.stop = False
			elif types == 6: # pulsamos la c
				if len(oldCell.connections) > 0:
					self.tcheck += oldCell.connections[0].number + oldCell.connections[-1].number
					self.oldcon = oldCell.connections
					for cell in oldCell.connections:
						self.cell_clear(cell)
						cell.connections = []
						cell.lines = cell.lines[:1]
			elif not self.stop: # si se presiona mov
				newCellRectY = (self.cellsprite.rect.y+(mov[1]*CELL_WIDTH))/CELL_WIDTH
				newCellRectX = (self.cellsprite.rect.x+(mov[0]*CELL_WIDTH))/CELL_WIDTH
				if newCellRectY < self.theight and newCellRectY >= 0 and newCellRectX >=0 and newCellRectX < self.twidth:
					newCell = self.table[newCellRectX][newCellRectY]
					# reglas de parada PRE
					if (newCell.number != 0 and ((len(self.history) > 0 and (newCell.color != self.history[0].color or newCell.number != self.history[0].number)) or (len(self.history) > 0 and len(self.history)+1 != self.history[0].number))) or (space and (newCell in self.history or len(newCell.connections) != 0 or len(oldCell.connections) != 0)):
						self.stop = True
					if newCell.number_color == GREY and newCell == self.history[-2]: # ir hacia detras
						self.stop = False
					if not self.stop and space:
						if types == 1: # abajo
							oldCell.lines.append(oldCell.rect.midbottom)
							self.cell_move(newCell)
							newCell.lines.append(newCell.rect.midtop)
						elif types == 2: # arriba
							oldCell.lines.append(oldCell.rect.midtop)
							self.cell_move(newCell)
							newCell.lines.append(newCell.rect.midbottom)
						elif types == 3: # izquierda
							oldCell.lines.append(oldCell.rect.midleft)
							self.cell_move(newCell)
							newCell.lines.append(newCell.rect.midright)
						elif types == 4: # derecha
							oldCell.lines.append(oldCell.rect.midright)
							self.cell_move(newCell)
							newCell.lines.append(newCell.rect.midleft)
						newCell.lines.append(self.cellsprite.cell.rect.center)
						if newCell.number != 0:
							if newCell.number_color == GREY: # ir hacia detras
								self.cell_clear(oldCell)
								oldCell.number = 0
								oldCell.number_color = BLACK
								self.history = self.history[0:-2]
								newCell.lines = newCell.lines[0:-3]
								oldCell.lines = oldCell.lines[0:1]
							else:
								self.cell_draw(newCell, newCell.color)
						else:
							newCell.background_color = WHITE
							newCell.number_color = GREY
							newCell.number = len(self.history)+1
						self.history.append(newCell)
					elif not self.stop and not space: # movimiento
						self.cell_move(newCell)
				self.stop = False
			oldCell = self.cellsprite.cell
			# reglas de parada POST
			if space and (len(self.history) > 0 and len(self.history) == self.history[0].number): 
				self.stop = True
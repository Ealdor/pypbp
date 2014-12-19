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
from constants import *

class Cell():
	""" Clase que representa una celda

    Args:
        posx(int): posicion horizontal
        posy(int): posicion vertical
        number(int): numero
        color(Color): color siempre

    Attributes:
    	background_color(set): color del fondo
    	border_color(set): color del borde
    	border_color_sprite(set): color del sprite de seleccion
    	number_color(set): color del número
    	lines_color(set): color de las lineas de conexion
    	rect(Rect): rectangulo de la celda
    	connections(list): lista de Celdas conectadas. Todas
    	lines(list): lista con las lineas de conexion
    	bsize(int): tamaño del borde
    	lsize(int): tamaño de las lineas de conexion

    """

	def __init__(self, posx, posy, number, color=WHITE):
		self.posx = posx
		self.posy = posy
		self.number = number
		self.color = color
		self.background_color = WHITE
		self.border_color = GREY2
		self.border_color_sprite = RED
		self.number_color = color
		self.lines_color = color
		self.rect = pygame.Rect(self.posx, self.posy, CELL_WIDTH, CELL_WIDTH)
		self.connections = []
		self.lines = [self.rect.center]
		self.bsize = 2
		self.lsize = 4

class CellSprite(pygame.sprite.Sprite):
	""" Clase que representa el sprite de selección

    Args:
        cell(Cell): celda actual
        bsize(int): tamaño del borde

    Attributes:
    	image(Surface): superficie de la celda
    	rect(Rect): rectangulo de la superficie

    """

	def __init__(self, cell, bsize):
		pygame.sprite.Sprite.__init__(self)
		self.cell = cell
		self.bsize = bsize
		self.image = pygame.Surface([CELL_WIDTH, CELL_WIDTH])
		pygame.draw.rect(self.image, self.cell.border_color_sprite, (0, 0, CELL_WIDTH, CELL_WIDTH), self.bsize)
		self.rect = self.image.get_rect()
		self.rect.x = self.cell.posx
		self.rect.y = self.cell.posy
		self.image.set_colorkey(BLACK)
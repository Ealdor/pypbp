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
from init import *
from table import *

if __name__ == '__main__':
	if len(sys.argv) == 2:
		ncol, nrow, tab = init_puzzle(sys.argv[1])
	else:
		sys.exit()

	# INICIALIZAMOS PYGAME
	init_pygame()
	screen = pygame.display.set_mode((1024, 600), pygame.RESIZABLE)
	pygame.display.set_caption('Pypbp 0.3')
	
	# CREAMOS UN TABLERO NUEVO
	table = Table(ncol, nrow, 1, 1, tab, screen)

	# BUCLE INFINITO
	loop = wep = True
	while loop:
		if wep: # solo actualizamos i ha habido algun cambio
			table.draw()
			wep = False
		pygame.display.flip()
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE):
				loop = False
			elif event.type == pygame.locals.KEYDOWN or event.type == pygame.locals.KEYUP:
				wep = table.check(event)
			elif event.type == pygame.VIDEORESIZE:
				table.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
				table.draw()
	sys.exit()
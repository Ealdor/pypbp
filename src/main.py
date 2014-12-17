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

import Tkinter as tk
import tkFileDialog
import sys
import pygame
import pygame.locals
import init
from init import *
from table import *

class Application(tk.Frame):
	""" Clase de la aplicación tkinter

	Attributes:
    	name(StringVar): nombre del puzzle elegido
    	types(StringVar): tipo de puzzle
    	status(StringVar): dimensiones del puzzle
    	completeName(string): ruta completa que devuelve tkFileDialog

    """

	def __init__(self, master = None):
		tk.Frame.__init__(self, master)
		self.grid()
		self.name = tk.StringVar()
		self.types = tk.StringVar()
		self.status = tk.StringVar()
		self.ones = tk.IntVar()
		self.completeName = ""
		self.name.set("Puzzle: -")
		self.status.set("Dimensiones: -")
		self.types.set("Tipo: -")
		self.createWidgets()

	def createWidgets(self):
		""" Función que crea y posiciona los widgets del tkinter """

		# Label instrucción
		self.instructionLabel = tk.Label(self, text = "Para jugar un nuevo puzzle, selecciona 'Examinar ficheros' y elige el fichero .csv (b&w) o .json (color).")
		self.instructionLabel.grid(padx = 10, pady = 10, column = 0, row = 0, columnspan = 2)
		# Frame opciones
		self.opLabel = tk.LabelFrame(self, text = "Opciones", padx = 10, pady = 10)
		self.opLabel.grid(sticky = tk.N, padx = 10, pady = 0, column = 1, row = 1)
		# Check unos rellenos
		self.onesCheck = tk.Checkbutton(self.opLabel, text = " Rellenar unos automáticamente", variable = self.ones)
		self.onesCheck.grid(padx = 10, column = 0, row = 0)
		# Frame jugar
		self.genLabel = tk.LabelFrame(self, text = "Jugar", padx = 10, pady = 10)
		self.genLabel.grid(sticky = tk.N, padx = 10, pady = 0, column = 0, row = 1)
		self.genLabel.columnconfigure(1, pad = 10)
		self.genLabel.rowconfigure(1, pad = 20)
		# Label puzzlename
		self.nameLabel = tk.Label(self.genLabel, textvariable = self.name, justify = tk.LEFT, width = 50)
		self.nameLabel.grid(sticky = tk.NW, padx = 10, column = 0, row = 0, columnspan = 2)
		# Botón jugar
		self.startButton = tk.Button(self.genLabel, text = 'Jugar', command = self.start, state = "disabled")
		self.startButton.grid(sticky = tk.W+tk.E, padx = 10, column = 1, row = 1, pady = 0)
		# Botón examinar
		self.browseButton = tk.Button(self.genLabel, text = 'Examinar ficheros', command = self.popup)
		self.browseButton.grid(sticky = tk.W+tk.E, padx = 10, column = 0, row = 1)
		# Label estado
		self.statusLabel = tk.Label(self.genLabel, textvariable = self.status, justify = tk.LEFT)
		self.statusLabel.grid(sticky = tk.NW, padx = 10, column = 0, row = 2, columnspan = 2)
		# Label tipo
		self.typesLabel = tk.Label(self.genLabel, textvariable = self.types, justify = tk.LEFT)
		self.typesLabel.grid(sticky = tk.NW, padx = 10, column = 0, row = 3, columnspan = 2)
		# Botón salir
		self.quitButton = tk.Button(self, text = 'Salir', command = self.quit, width = 10)
		self.quitButton.grid(sticky = tk.W, padx = 10, pady = 10)

	def popup(self):
		""" Función cuando se pulsa el boton de examinar ficheros """

		self.completeName = tkFileDialog.askopenfilename(initialdir = "puzzles", filetypes = [("Bitmap", "*.csv"), ("Bitmap", "*.json")])
		if self.completeName != "" and self.completeName != ():
			self.startButton.config(state = 'normal')
			self.name.set("Puzzle: " + string.rsplit(self.completeName, "/")[-1])
			if len(self.name.get()) >= 60:
				self.name.set(self.name.get()[0:59] + "...")
			typef = string.rsplit(string.rsplit(self.completeName, "/")[-1], ".")[-1]
			ncol, nrow, tab = init_puzzle(self.completeName)
			self.status.set("Dimensiones: {0} x {1}".format(ncol, nrow))
			if typef == "csv":
				self.types.set("Tipo: blanco y negro")
			else:
				self.types.set("Tipo: color")

	def start(self):
		""" Función cuando se pulsa el botón de jugar """

		# INICIALIZAMOS PYGAME
		init_pygame()
		screen = pygame.display.set_mode((1024, 600), pygame.RESIZABLE)
		pygame.display.set_caption('Pypbp 1.0')
		# CREAMOS UN TABLERO NUEVO
		ncol, nrow, tab = init_puzzle(self.completeName, self.ones.get())
		table = Table(ncol, nrow, 1, 1, tab, screen)
		# BUCLE INFINITO
		loop = wep = True
		while loop:
			if wep: # solo actualizamos si ha habido algun movimiento
				table.draw()
				wep = False
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT or (event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE):
					loop = False
				elif event.type == pygame.locals.KEYDOWN or event.type == pygame.locals.KEYUP:
					wep = table.check(event)
				elif event.type == pygame.VIDEORESIZE: # si se cambia el tamaño de la ventana
					table.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
					wep = True
		pygame.quit()

app = Application()
app.master.title('Pypbp 1.0')
app.mainloop()
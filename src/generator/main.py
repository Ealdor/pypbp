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
import string
import generator
import time
import utils

class Application(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.grid()
		
		self.name = tk.StringVar()
		self.name.set("Puzzle: -")
		self.status = tk.StringVar()
		self.status.set("Estado: -")
		self.leng = tk.StringVar()
		self.leng.set("Iteración: -/- y Número: -/-")
		self.totaltime = tk.StringVar()
		self.totaltime.set("Tiempo total: -")
		self.ones = tk.StringVar()
		self.ones.set("Total de unos: -")
		self.types = tk.StringVar()
		self.types.set("Progreso: -")

		self.completeName = ""
		self.createWidgets()
		self.g = None

	def createWidgets(self):
		# Label instrucción
		self.instructionLabel = tk.Label(self, text = "Para generar un nuevo puzzle, selecciona 'Examinar ficheros' y elige el fichero .csv (b&w) o .json (color).\nElige el número máximo y la complejidad. A mayores valores, mayor tiempo de generación.\nEl fichero resultante 'temp.csv' o 'temp.json' estará en el directorio del generador.")
		self.instructionLabel.grid(padx = 10, pady = 10, column = 0, row = 0, columnspan = 2)

		# Frame option
		self.browseLabel = tk.LabelFrame(self, text = "Opciones de generación", padx = 10, pady = 10)
		self.browseLabel.grid(sticky = tk.N, padx = 10, pady = 0, column = 0, row = 1)
		self.browseLabel.columnconfigure(1, pad = 10)
		self.browseLabel.rowconfigure(4, pad = 10)
		# Botón examinar
		self.browseButton = tk.Button(self.browseLabel, text = 'Examinar ficheros', command = self.popup)
		self.browseButton.grid(padx = 10, column = 0, row = 0)
		# Label maxnumber
		self.maxnumberLabel = tk.Label(self.browseLabel, text = "Número máximo (2 - 21):")
		self.maxnumberLabel.grid(sticky = tk.NW, padx = 10, column = 0, row = 1, pady = 10)
		# Spinbox maxnumber
		self.maxnumberSpinbox = tk.Spinbox(self.browseLabel, from_ = 2, to_ = 21, wrap = True, width = 2)
		self.maxnumberSpinbox.grid(sticky = tk.NW, padx = 10, column = 0, row = 2, pady = 0)
		# Label complejidad
		self.complexLabel = tk.Label(self.browseLabel, text = "Complejidad (1 - 5):")
		self.complexLabel.grid(sticky = tk.NW, padx = 10, column = 0, row = 3, pady = 10)
		# Spinbox dificuñtad
		self.complexSpinbox = tk.Spinbox(self.browseLabel, from_ = 1, to_ = 5, wrap = True, width = 2)
		self.complexSpinbox.grid(sticky = tk.NW, padx = 10, column = 0, row = 4, pady = 1)

		# Frame generacion
		self.genLabel = tk.LabelFrame(self, text = "Generación", padx = 10, pady = 10)
		self.genLabel.grid(sticky = tk.N, padx = 10, pady = 0, column = 1, row = 1)
		self.genLabel.columnconfigure(1, pad = 10)
		self.genLabel.rowconfigure(1, pad = 20)
		# Label puzzlename
		self.nameLabel = tk.Label(self.genLabel, textvariable = self.name, justify = tk.LEFT, width = 50)
		self.nameLabel.grid(sticky = tk.NW, padx = 10, column = 0, row = 0, columnspan = 2)
		# Botón generar
		self.startButton = tk.Button(self.genLabel, text = 'Empezar', command = self.start, state = "disabled")
		self.startButton.grid(sticky = tk.W+tk.E, padx = 10, column = 0, row = 1, pady = 0)
		# Botón cancelar
		self.cancelButton = tk.Button(self.genLabel, text = 'Cancelar', command = self.cancel, state = "disabled")
		self.cancelButton.grid(sticky = tk.W+tk.E, padx = 10, column = 1, row = 1, pady = 0)
		# Label estado
		self.statusLabel = tk.Label(self.genLabel, textvariable = self.status, justify = tk.LEFT)
		self.statusLabel.grid(sticky = tk.NW, padx = 10, column = 0, row = 2, columnspan = 2)
		# Label longitud
		self.lengLabel = tk.Label(self.genLabel, textvariable = self.leng, justify = tk.LEFT)
		self.lengLabel.grid(sticky = tk.NW, padx = 10, column = 0, row = 4, columnspan = 2)
		# Label tiempo total
		self.totaltimeLabel = tk.Label(self.genLabel, textvariable = self.totaltime, justify = tk.LEFT)
		self.totaltimeLabel.grid(sticky = tk.NW, padx = 10, column = 0, row = 6, columnspan = 2)
		# Label numero de unos
		self.onesLabel = tk.Label(self.genLabel, textvariable = self.ones, justify = tk.LEFT)
		self.onesLabel.grid(sticky = tk.NW, padx = 10, column = 0, row = 5, columnspan = 2)
		# Label tipo
		self.typesLabel = tk.Label(self.genLabel, textvariable = self.types, justify = tk.LEFT)
		self.typesLabel.grid(sticky = tk.NW, padx = 10, column = 0, row = 3, columnspan = 2)

		# Botón quit
		self.quitButton = tk.Button(self, text = 'Salir', command = self.quit, width = 10)
		self.quitButton.grid(sticky = tk.W, padx = 10, pady = 10)

	def popup(self):
		self.completeName = tkFileDialog.askopenfilename(initialdir = "puzzles", filetypes = [("Bitmap", "*.csv"), ("Bitmap", "*.json")])
		if self.completeName != "" and self.completeName != ():
			self.startButton.config(state = 'normal')
			self.name.set("Puzzle: " + string.rsplit(self.completeName, "/")[-1])
			if len(self.name.get()) >= 60:
				self.name.set(self.name.get()[0:59] + "...")

	def start(self):
		self.status.set("Estado: -")
		self.leng.set("Iteración: -/- y Número: -/-")
		self.totaltime.set("Tiempo total: -")
		self.ones.set("Total de unos: -")
		self.types.set("Progreso: -")
		self.startButton.config(state = 'disabled')
		self.browseButton.config(state = 'disabled')
		self.cancelButton.config(state = 'normal')
		self.maxnumberSpinbox.config(state = 'disabled')
		self.complexSpinbox.config(state = 'disabled')
		if int(self.complexSpinbox.get()) in (1,2,3,4,5) and int(self.maxnumberSpinbox.get()) in (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21) and self.completeName != "":
			start_time = time.time()
			if self.name.get().split('.')[1] == 'csv':
				self.g = generator.Generator(self.maxnumberSpinbox.get(), self.complexSpinbox.get(), utils.read_csv(self.completeName), self.cancelButton, self.types)
			else:
				self.g = generator.Generator(self.maxnumberSpinbox.get(), self.complexSpinbox.get(), utils.read_json(self.completeName), self.cancelButton, self.types)
			self.g.count_one()
			self.ones.set("Total de unos: {0}".format(len(self.g.table_uno)))
			i = 0
			while self.g.maxim > 1:
				i += 1
				self.leng.set("Iteración: {0}/{1} y Número: {2}".format(i, self.complexSpinbox.get(), self.g.maxim))
				self.status.set("Estado: Generando puzzle...")
				self.g.step_one()
				tim = utils.sec_to(int(time.time() - start_time))
				self.totaltime.set("Tiempo total: {0}h:{1}m:{2}s".format(tim[0], tim[1], tim[2]))
				self.status.set("Estado: Aplicando condición uno...")
				self.g.cond_dos(1)
				tim = utils.sec_to(int(time.time() - start_time))
				self.totaltime.set("Tiempo total: {0}h:{1}m:{2}s".format(tim[0], tim[1], tim[2]))
				self.status.set("Estado: Aplicando condición dos...")
				self.g.cond_dos(2)
				tim = utils.sec_to(int(time.time() - start_time))
				self.totaltime.set("Tiempo total: {0}h:{1}m:{2}s".format(tim[0], tim[1], tim[2]))
				
				if self.g.maxim >= 4:
					self.status.set("Estado: Aplicando condición tres...")
					self.g.cond_dos(3)
					tim = utils.sec_to(int(time.time() - start_time))
					self.totaltime.set("Tiempo total: {0}h:{1}m:{2}s".format(tim[0], tim[1], tim[2]))
				
				self.g.count_one()
				self.ones.set("Total de unos: {0}".format(len(self.g.table_uno)))
				if i == self.g.iters:
					self.g.maxim -= 1
					i = 0
			if self.name.get().split('.')[1] == 'csv':
				utils.write_csv(self.g.table_all)
			else:
				utils.write_json(self.g.table_all)

			if self.g.cancel:
				self.status.set("Estado: Cancelado")
			else:
				self.status.set("Estado: Completado")
			self.g = None
		self.startButton.config(state = 'normal')
		self.browseButton.config(state = 'normal')
		self.cancelButton.config(state = 'disabled')
		self.maxnumberSpinbox.config(state = 'normal')
		self.complexSpinbox.config(state = 'normal')

	def cancel(self):
		if self.g and not self.g.cancel: 
			self.g.cancel = True
			self.g.maxim = 1
			self.status.set("Estado: Cancelando...")

app = Application()
app.master.title('Pypbp - Generador')
app.mainloop()
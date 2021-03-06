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

""" This module implements the JSON file generation functionality for a given image.
	Image format support: JPG, PNG, GIF (non animated), BMP, PCX, TGA (uncompressed), TIF, LBM (and PBM), PBM (and PGM, PPM), XPM
	Output: the JSON file ready for use with the generator module or the puzzle core (will only contains '1'(color) and '0'(white) tho).
	
	Command line interface:
		$ python img_to_json.py [IMAGEN_NAME.json] [WIDTH] [HEIGHT] """

import sys
import json
import pygame

def generate_json(fname, ncol, nrow):
	f = open(fname.split('.')[0]+".json", 'w')
	simage = pygame.image.load(fname)
	rows = []
	for x in xrange(0, nrow):
		cols = []
		for y in xrange(0, ncol):
			pixcolor = simage.get_at((y,x))
			if (pixcolor.r,pixcolor.g,pixcolor.b) == (255, 255, 255): #blanco
				cols.append({'color':{'r':255,'b':255,'g':255},'number':0})
			else:
				cols.append({'color':{'r':pixcolor.r,'b':pixcolor.b,'g':pixcolor.g},'number':1})
		rows.append(cols)
	json.dump(rows, f)
	f.close()

if __name__ == '__main__':
	if len(sys.argv) == 4:
		generate_json(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
	else:
		print "Use: python img_to_json.py [IMAGEN_NAME.type] [WIDTH] [HEIGHT]"
		sys.exit()
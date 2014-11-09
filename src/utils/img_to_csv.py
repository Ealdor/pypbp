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

""" This module implements the CSV file generation functionality for a given image.
	Image format support: JPG, PNG, GIF (non animated), BMP, PCX, TGA (uncompressed), TIF, LBM (and PBM), PBM (and PGM, PPM), XPM
	Output: the CSV file ready for use with the generator module or the puzzle core (will only contains '1'(black) and '0'(white) tho).
	
	Command line interface:
		$ python img_to_csv.py [IMAGEN_NAME.csv] [WIDTH] [HEIGHT] """

import sys
import pygame

def generate_csv(fname, ncol, nrow):
	f = open(fname.split('.')[0]+".csv", 'w')
	simage = pygame.image.load(fname)
	for x in xrange(0, nrow):
		for y in xrange(0, ncol):
			pixcolor = simage.get_at((y,x))
			if (pixcolor.r,pixcolor.g,pixcolor.b) == (255, 255, 255): # blanco
				f.write('0')
			else: 
				f.write('1')
			if y == ncol-1: f.write('\n')
			else: f.write(',')
	f.close()

if __name__ == '__main__':
	if len(sys.argv) == 4:
		generate_csv(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
	else:
		print "Use: python img_to_csv.py [IMAGEN_NAME.type] [WIDTH] [HEIGHT]"
		sys.exit()

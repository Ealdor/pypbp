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

import pygame
import pygame.locals

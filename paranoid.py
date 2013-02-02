#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# paranoid - compton configuration GUI
# Copyright (C) 2013  Giuseppe "GsC_RuL3Z" Corti
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from gi.repository import Gtk
import gobject
#import os
import re

GUIFILE = "./paranoid.glade"
COMPTON = "compton.conf"

def getbool(value):
	# Function to find and return boolean variables from compton.conf
	for line in open(COMPTON, 'r'):
		if re.search(value,line) != None:
			if re.search("true",line) != None:
				return True
			else:
				return False
				
def getint(value):
	# Function to find and return values from compton.conf
	for line in open(COMPTON, 'r'):
		if re.search(value,line) != None:
			# Clear the line
			result = line.replace(value,"")
			result = result.replace(" ","")
			result = result.replace("=","")
			result = result.replace(";\n","")

			# Return integer value
			return int(result)
			
def invertbool(bool):
	# Some values such as no-dock-shadow need to be inverted
	if bool == True:
		return False
	else:
		return True

class GUI():
	def __init__(self, donotshow=False):
		
		# GUI setup
		self.builder = Gtk.Builder()
		self.builder.add_from_file(GUIFILE)

		# Get main window
		self.main = self.builder.get_object("main")
		
		#
		# Shadow
		#
		# Get Box
		self.shadow_box = self.builder.get_object("shadow-box")

		# Main switch 
		self.shadow = self.builder.get_object("shadow")
		self.shadow.set_active(getbool("shadow"))
		self.shadow.connect("button-press-event", self.shadow_switch)
		
		# Panel shadow bool
		self.panel_shadow = self.builder.get_object("panel_shadow")
		self.panel_shadow.set_active(invertbool(getbool("no-dock-shadow")))

		# Clear shadow bool
		self.clear_shadow = self.builder.get_object("clear_shadow")
		self.clear_shadow.set_active(getbool("clear-shadow"))

		# Radius scale
		self.radius = self.builder.get_object("radius")
		self.radius.set_range(0, 25)
		self.radius.set_value(getint("shadow-radius"))

		#
		# Fading
		#
        # Main switch
		self.fading = self.builder.get_object("fading")
		self.fading.set_active(getbool("fading"))
		self.fading.connect("button-press-event", self.fading_switch)

		#
		# Opacity
		#
		# todo

		# Connect destroy
		self.main.connect("destroy", lambda x: Gtk.main_quit())

		# Exit button
		self.exit = self.builder.get_object("exit")
		self.exit.connect("clicked", Gtk.main_quit)

		# Save & apply button
		self.save = self.builder.get_object("save")


		# Show it
		if not donotshow: self.main.show_all()

	def fading_switch(self, obj, opt = None):
		# Switch Fading on/off

	def shadow_switch(self, obj, opt = None):

		# Switch Shadow on/off
		self.shadow_box.set_sensitive(invertbool(self.shadow.get_active()))
	

if __name__ == "__main__":
	g = GUI()
	Gtk.main()

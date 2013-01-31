#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Gdk
import gobject
#import os
import re

GUIFILE = "./paranoid.glade"
COMPTON = "compton.conf"

def getbool(value):
	for line in open(COMPTON, 'r'):
		if re.search(value,line) != None:
			if re.search("true",line) != None:
				return True
			else:
				return False
				
def getint(value):
	for line in open(COMPTON, 'r'):
		if re.search(value,line) != None:
			result = line.replace(value,"")
			result = result.replace(" ","")
			result = result.replace("=","")
			result = result.replace(";\n","")
			return int(result)
			
def invertbool(bool):
	if bool == True:
		return False
	else:
		return True

class GUI():
	def __init__(self, donotshow=False):
		
		self.builder = Gtk.Builder()
		self.builder.add_from_file(GUIFILE)

		# Get main window
		self.main = self.builder.get_object("main")

		#
		# Shadow
		#
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
          
		# Connect destroy
		self.main.connect("destroy", lambda x: Gtk.main_quit())

		# Show it
		if not donotshow: self.main.show_all()

	def shadow_switch(self, obj, asd=None):
			
		if self.shadow.get_active():
			status=False
		else:
			status=True

		self.panel_shadow.set_sensitive(status)
		self.clear_shadow.set_sensitive(status)
		self.radius.set_sensitive(status)

if __name__ == "__main__":
	g = GUI()
	Gtk.main()
	

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Paranoid - GTK+3 configuration tool for compton.
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
from threading import Thread
import gobject
import os
import re
import string

GUIFILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "paranoid.glade")
COMPTON = os.getenv('HOME') + "/.config/compton.conf"
AUTOSTART = os.getenv('HOME') + "/.config/.composite_enabled"
newconf = False

class RestartCompton(Thread):
	def __init__(self, parent):
		
		self.parent = parent
		
		Thread.__init__(self)
		
	def run(self):
		
		os.system("pkill compton")
		
		# Start only if we are sure the effects are enabled.
		if self.parent.main_switch.get_active():
			os.system("compton -b")


def getbool(value):
	# Function to find and return boolean variables from compton.conf
	lines = 0
	for line in open(COMPTON, 'r'):
		if re.search(value,line) != None:
			if re.search(value + " = true;",line) != None:
				return True
			else:
				return False
		else:
			if lines == conflen():
				return False
		lines += 1
		
def conflen():
	# Count compton.conf lines
	lines = 0
	for line in open(COMPTON, 'r'):
		lines += 1
	return lines-1
				
def getint(value):
	# Function to find and return values from compton.conf
	lines = 0
	for line in open(COMPTON, 'r'):
		if re.search(value,line) != None:
			# Clear the line
			result = line.replace(value,"")
			result = result.replace(" ","")
			result = result.replace("=","")
			result = result.replace(";","")

			# Return float value
			# Many values like menu-opacity are float 
			return float(result)
		else:
			if lines == conflen():
				return 0
		lines +=1

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

		# Get main switch
		self.main_switch = self.builder.get_object("de-effects")	
		self.main_switch.connect("button-press-event", self.main_switch_event)
		if os.path.isfile(AUTOSTART):
			self.main_switch.set_active(True)

		# Get main notebook
		self.notebook = self.builder.get_object("notebook")		
	
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
		# Get Box
		self.fading_box = self.builder.get_object("fading-box")

		# Main switch
		self.fading = self.builder.get_object("fading")
		self.fading.set_active(getbool("fading"))
		self.fading.connect("button-press-event", self.fading_switch)

		# No fading openclose
		self.fading_openclose = self.builder.get_object("fading-openclose")
		self.fading_openclose.set_active(invertbool(getbool("no-fading-openclose")))

		# Fade delta scale
		self.fade_delta = self.builder.get_object("fade-delta")
		self.fade_delta.set_range(0, 30)
		self.fade_delta.set_value(getint("fade-delta"))

		#
		# Opacity
		#
		# Menu opacity scale
		self.menu_opacity = self.builder.get_object("menu-opacity")
		self.menu_opacity.set_range(0, 10)
		self.menu_opacity.set_value(getint("menu-opacity")*10)

		# Inactive opacity scale
		self.inactive_opacity = self.builder.get_object("inactive-opacity")
		self.inactive_opacity.set_range(0, 10)
		self.inactive_opacity.set_value(getint("inactive-opacity")*10)

		# Frame opacity scale
		self.frame_opacity = self.builder.get_object("frame-opacity")
		self.frame_opacity.set_range(0, 10)
		self.frame_opacity.set_value(getint("frame-opacity")*10)

		#
		# Other
		#
		# Inactive opacity override 
		self.inactive_opacity_override = self.builder.get_object("inactive-opacity-override")
		self.inactive_opacity_override.set_active(getbool("inactive-opacity-override"))

		# Sahdow ignore shaped
		self.shadow_ignore_shaped = self.builder.get_object("shadow-ignore-shaped")
		self.shadow_ignore_shaped.set_active(getbool("shadow-ignore-shaped"))

		# Mark wmwin focused
		self.mark_wmwin_focused = self.builder.get_object("mark-wmwin-focused")
		self.mark_wmwin_focused.set_active(getbool("mark-wmwin-focused"))

		# Detect rounded corners
		self.detect_rounded_corners = self.builder.get_object("detect-rounded-corners")
		self.detect_rounded_corners.set_active(getbool("detect-rounded-corners"))

		# Blur background fixed
		self.blur_background_fixed = self.builder.get_object("blur-background-fixed")
		self.blur_background_fixed.set_active(getbool("blur-background-fixed"))

		# Connect destroy
		self.main.connect("destroy", lambda x: Gtk.main_quit())

		# Save & apply button
		self.save = self.builder.get_object("save")
		self.save.connect("clicked", self.save_apply)

		# Defaults button
		self.defaults_button = self.builder.get_object("defaults_button")
		self.defaults_button.connect("clicked", self.defaults_button_execute)

		# Get sensitive
		if newconf == False:
			self.view()
		else:
			self.defaults_settings()
			self.main_switch.set_active(False) # If it is new, the user still hasn't chosen to enable compositing.
			self.notebook.set_sensitive(False)

		# Show it
		if not donotshow: self.main.show_all()

	def defaults_button_execute(self, obj, opt = None):
		self.defaults_settings()

	def view(self):
		# Setting up objects sensitive
		# Generate default settings if compton.conf doesn't exist
						
		# Shadow panel sensitive
		if self.shadow.get_active() == False:
			self.shadow_box.set_sensitive(False)
		else:
			self.shadow_box.set_sensitive(True)

		# Fade panel sensitive
		if self.fading.get_active() == False:
			self.fading_box.set_sensitive(False)
		else:
			self.fading_box.set_sensitive(True)

		# Notebook sensitive
		if self.main_switch.get_active() == False:
			self.notebook.set_sensitive(False)
		else:
			self.notebook.set_sensitive(True)

	def defaults_settings(self):
		# Restore compton.conf default value
		# Shadow settings
		self.main_switch.set_active(True)
		self.shadow.set_active(True)
		self.panel_shadow.set_active(False)
		self.clear_shadow.set_active(False)
		self.radius.set_value(12)
		# Fade settings
		self.fading.set_active(False)
		self.fading_openclose.set_active(False)
		self.fade_delta.set_value(12)
		# Opacity settings
		self.menu_opacity.set_value(10)
		self.inactive_opacity.set_value(10)
		self.frame_opacity.set_value(10)
		# Other settings
		self.inactive_opacity_override.set_active(False)
		self.shadow_ignore_shaped.set_active(False)
		self.mark_wmwin_focused.set_active(True)
		self.detect_rounded_corners.set_active(True)
		self.blur_background_fixed.set_active(False)

		# Get sensitive
		self.view()

	def main_switch_event(self, obj, opt = None):
		# Switch Desktop effects on/off
		self.notebook.set_sensitive(invertbool(self.main_switch.get_active()))

		if os.path.isfile(AUTOSTART):
			# Delete .composite_enabled 
			os.remove(AUTOSTART)
		else:
			# Touch .composite_enabled
			enabled_file = open(AUTOSTART,'w+')
			enabled_file.write("# Paranoid composite enabled\n# delete this file to disable composite manager\n")
			enabled_file.close()

	def fading_switch(self, obj, opt = None):
		# Switch Fading on/off
		self.fading_box.set_sensitive(invertbool(self.fading.get_active()))	

	def shadow_switch(self, obj, opt = None):
		# Switch Shadow on/off
		self.shadow_box.set_sensitive(invertbool(self.shadow.get_active()))

	def thread_killcompton(self):
		thrd = RestartCompton(self)
		thrd.start()
	
	def save_apply(self, obj):
		# Save & apply click event
		# this should write the new configuration into compton.conf
		# Insert value into dictionary
		settings2file = [['shadow',self.shadow.get_active()], # shadow settings
		['no-dock-shadow' , invertbool(self.panel_shadow.get_active())],
		['clear-shadow' , self.clear_shadow.get_active()],
		['shadow-radius', self.radius.get_value()],
		['fading', self.fading.get_active()], # fade settings
		['no-fading-openclose', invertbool(self.fading_openclose.get_active())],
		['fade-delta', self.fade_delta.get_value()], 
		['menu-opacity', self.menu_opacity.get_value()/10], # opacity settings
		['inactive-opacity', (self.inactive_opacity.get_value()/10.0)],
		['frame-opacity', (self.frame_opacity.get_value()/10.0)], 
		['inactive-opacity-override', self.inactive_opacity_override.get_active()], # other settings
		['shadow-ignore-shaped', self.shadow_ignore_shaped.get_active()],
		['mark-wmwin-focused', self.mark_wmwin_focused.get_active()],
		['blur-background-fixed', self.blur_background_fixed.get_active()],
		['detect-rounded-corners', self.detect_rounded_corners.get_active()]]

		#print settings2file[7][1]/10

		# Open and read old configuration file
		old_config_file = open(COMPTON,'r')
		old_config = old_config_file.read()
		old_config_file.close()

		# Replace old values with new inputs
		# Shadow settings
		for i in range(0,settings2file.__len__()): #14
			string_start = "\n"+settings2file[i][0]+r" =(.*);"
			if re.search(string_start,old_config):
				if isinstance(settings2file[i][1],bool):
					old_config = (re.sub(string_start, "\n" + settings2file[i][0]+" = %r;" % settings2file[i][1], old_config))
				elif isinstance(settings2file[i][1],float):
					old_config = (re.sub(string_start, "\n" + settings2file[i][0]+" = %f;" % settings2file[i][1], old_config))
			else: 
				old_config = old_config + "\n" + settings2file[i][0] + " = " + str(settings2file[i][1]) + ";"
			
		# Fix uppercase
		old_config = (re.sub("False","false",old_config))
		old_config = (re.sub("True","true",old_config))

		# Float fix?
		old_config = (re.sub("00000","",old_config))

		# Debug
		#print old_config

		# Write new configuration file
		new_config_file = open(COMPTON,'w+')
		new_config_file.write(old_config)
		new_config_file.close()

		# Restart compton
		self.thread_killcompton()
		self.main.destroy()

		# close Paranoid
		Gtk.main_quit()

if __name__ == "__main__":

	if not os.path.isfile(COMPTON):
		
		compton_file = open(COMPTON,'w+')
		compton_file.write("# compton.conf created by paranoid\n")
		compton_file.close()
		newconf = True

	g = GUI()
	Gtk.main()

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

from gi.repository import Gtk, GObject
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

def isValue(item, value):
	""" Returns True if item is value, False if not. """

	if not item in defaults or defaults[item] != value:
		return False
	else:
		return True

def getBool(value):
	""" Returns the value if in defaults, False if not. """

	if value in defaults:
		return defaults[value]
	else:
		return False

def getInt(value):
	""" Returns the value if in defaults, 0 if not. """
	
	if value in defaults:
		return defaults[value]
	else:
		return 0

def invertBool(bool):
	""" Inverts bool. """

	if bool == True:
		return False
	else:
		return True

def isInt(item):
	"""Returns True if item is an integer, False if not."""
	
	if type(item) == int or item.strip("+-").isdigit():
		return True
	else:
		return False

def isBool(item):
	""" Returns True if item is a boolean object, False if not. """
	
	if type(item) == bool or item.lower() in ("true","false","0","1"):
		return True
	else:
		return False

def boolFromString(item):
	""" Returns a boolean object from a string which resembles one. """
	
	if isBool(item):
		if item.lower() in ("true", "1"):
			return True
		elif item.lower() in ("false", "0"):
			return False
	
	return None

def isFloat(item):
	""" Returns True if item is a float object, False if not. """

	if type(item) == float or "." in item and isInt(item.replace(".","", 1)):
		return True
	else:
		return False

def returnValues():
	""" Returns every value in the config value """
	
	dct = {}
	if not os.path.exists(COMPTON): return dct
	
	with open(COMPTON, "r") as f:
		for line in f.readlines():
			line = line.replace(" ","").replace("\n","").replace("\r","").split("=")

			if len(line) != 2:
				# Unable to parse this line.
				continue
			
			item, value = line
						
			# Remove ; and " from value
			value = value.replace(";","").replace('"',"")
			
			# Convert value
			if isBool(value):				
				value = boolFromString(value)
			elif isFloat(value):
				value = float(value)
			elif isInt(value):
				value = int(value)
			
			# Add to dct
			dct[item] = value
	
	return dct

defaults = returnValues()

class GUI():
	def __init__(self, donotshow=False):
		
		# GUI setup
		self.builder = Gtk.Builder()
		self.builder.add_from_file(GUIFILE)

		# Get main window
		self.main = self.builder.get_object("main")

		# Get main notebook
		self.notebook = self.builder.get_object("notebook")		

		# Get main switch
		self.main_switch = self.builder.get_object("de-effects")	
		self.main_switch.connect("notify::active", self.main_switch_event)
		if os.path.isfile(AUTOSTART):
			self.main_switch.set_active(True)
	
		# Shadow
		#
		# Get Box
		self.shadow_box = self.builder.get_object("shadow-box")

		# Main switch 
		self.shadow = self.builder.get_object("shadow")
		self.shadow.set_active(getBool("shadow"))
		self.shadow.connect("notify::active", self.shadow_switch)
		
		# Panel shadow bool
		self.panel_shadow = self.builder.get_object("panel_shadow")
		self.panel_shadow.set_active(invertBool(getBool("no-dock-shadow")))

		# Clear shadow bool
		self.clear_shadow = self.builder.get_object("clear_shadow")
		self.clear_shadow.set_active(getBool("clear-shadow"))

		# Radius scale
		self.radius = self.builder.get_object("radius")
		self.radius.set_range(0, 25)
		self.radius.set_value(getInt("shadow-radius"))

		#
		# Fading
		#
		# Get Box
		self.fading_box = self.builder.get_object("fading-box")

		# Main switch
		self.fading = self.builder.get_object("fading")
		self.fading.set_active(getBool("fading"))
		self.fading.connect("notify::active", self.fading_switch)

		# No fading openclose
		self.fading_openclose = self.builder.get_object("fading-openclose")
		self.fading_openclose.set_active(invertBool(getBool("no-fading-openclose")))

		# Fade delta scale
		self.fade_delta = self.builder.get_object("fade-delta")
		self.fade_delta.set_range(0, 30)
		self.fade_delta.set_value(getInt("fade-delta"))

		#
		# Opacity
		#
		# Menu opacity scale
		self.menu_opacity = self.builder.get_object("menu-opacity")
		self.menu_opacity.set_range(0, 10)
		self.menu_opacity.set_value(getInt("menu-opacity")*10)

		# Inactive opacity scale
		self.inactive_opacity = self.builder.get_object("inactive-opacity")
		self.inactive_opacity.set_range(0, 10)
		self.inactive_opacity.set_value(getInt("inactive-opacity")*10)

		# Frame opacity scale
		self.frame_opacity = self.builder.get_object("frame-opacity")
		self.frame_opacity.set_range(0, 10)
		self.frame_opacity.set_value(getInt("frame-opacity")*10)

		#
		# Other
		#
		# Backend
		self.backend_combo = self.builder.get_object("backend-combobox")

		# Inactive opacity override 
		self.inactive_opacity_override = self.builder.get_object("inactive-opacity-override")
		self.inactive_opacity_override.set_active(getBool("inactive-opacity-override"))

		# Sahdow ignore shaped
		self.shadow_ignore_shaped = self.builder.get_object("shadow-ignore-shaped")
		self.shadow_ignore_shaped.set_active(getBool("shadow-ignore-shaped"))

		# Mark wmwin focused
		self.mark_wmwin_focused = self.builder.get_object("mark-wmwin-focused")
		self.mark_wmwin_focused.set_active(getBool("mark-wmwin-focused"))

		# Detect rounded corners
		self.detect_rounded_corners = self.builder.get_object("detect-rounded-corners")
		self.detect_rounded_corners.set_active(getBool("detect-rounded-corners"))

		# Blur background fixed
		self.blur_background_fixed = self.builder.get_object("blur-background-fixed")
		self.blur_background_fixed.set_active(getBool("blur-background-fixed"))

		# Connect destroy
		self.main.connect("destroy", lambda x: Gtk.main_quit())

		# Save & apply button
		self.save = self.builder.get_object("save")
		self.save.connect("clicked", self.save_apply)

		# Defaults button
		self.defaults_button = self.builder.get_object("defaults_button")
		self.defaults_button.connect("clicked", self.defaults_button_execute)

		# Setup GUI
		self.setup(newconf)

		# Get sensitive
		if newconf == False:
			self.view()
		else:
			self.defaults_settings()
			self.main_switch.set_active(False) # If it is new, the user still hasn't chosen to enable compositing.
			self.notebook.set_sensitive(False)

		# Show it
		if not donotshow: self.main.show_all()

	def setup(self, newconf):
		""" Initialize GUI """
		# Set backend combobox
		list_backend = Gtk.ListStore(GObject.TYPE_STRING)
		list_backend.append(("GLX",))
		list_backend.append(("XRender",))
		self.backend_combo.set_model(list_backend)
		cell = Gtk.CellRendererText()
		self.backend_combo.pack_start(cell, True)
		self.backend_combo.add_attribute(cell, "text", 0)

		# set backend value
		if newconf == False:
			if not isValue("backend","glx"):
				self.backend_combo.set_active(1)
			else:
				self.backend_combo.set_active(0)
		else:
			self.backend_combo.set_active(0)


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
		val = self.main_switch.get_active()
		self.notebook.set_sensitive(val)

		if not val and os.path.exists(AUTOSTART):
			# Delete .composite_enabled 
			os.remove(AUTOSTART)
		elif val and not os.path.exists(AUTOSTART):
			# Touch .composite_enabled
			with open(AUTOSTART, "w+") as f:
				f.write("# Paranoid composite enabled\n# delete this file to disable composite manager\n")

	def fading_switch(self, obj, opt = None):
		# Switch Fading on/off
		self.fading_box.set_sensitive(self.fading.get_active())	

	def shadow_switch(self, obj, opt = None):
		# Switch Shadow on/off
		self.shadow_box.set_sensitive(self.shadow.get_active())

	def thread_killcompton(self):
		thrd = RestartCompton(self)
		thrd.start()
	
	def combo2backend(self, value):
		""" Combobox value to backend compton config file value """
		if value == 0:
			return '"glx"'
		else:
			return '"xrender"'
	
	def save_apply(self, obj):
		# Save & apply click event
		# this should write the new configuration into compton.conf

		# Insert value into dictionary
		settings2file = {
			'shadow':self.shadow.get_active(), # shadow settings
			'no-dock-shadow' : invertBool(self.panel_shadow.get_active()),
			'clear-shadow' : self.clear_shadow.get_active(),
			'shadow-radius': self.radius.get_value(),
			'fading': self.fading.get_active(), # fade settings
			'no-fading-openclose': invertBool(self.fading_openclose.get_active()),
			'fade-delta': self.fade_delta.get_value(), 
			'menu-opacity': self.menu_opacity.get_value()/10, # opacity settings
			'inactive-opacity': (self.inactive_opacity.get_value()/10.0),
			'frame-opacity': (self.frame_opacity.get_value()/10.0), 
			'inactive-opacity-override': self.inactive_opacity_override.get_active(), # other settings
			'backend': self.combo2backend(self.backend_combo.get_active()), 
			'shadow-ignore-shaped': self.shadow_ignore_shaped.get_active(),
			'mark-wmwin-focused': self.mark_wmwin_focused.get_active(),
			'blur-background-fixed': self.blur_background_fixed.get_active(),
			'detect-rounded-corners': self.detect_rounded_corners.get_active()
		}
				
		#print settings2file[7][1]/10

		# Open and read old configuration file
		with open(COMPTON, "r") as f:
			old_config = f.read()
			if not old_config[-1] == "\n":
				old_config = old_config + "\n" # \n is a workaround for old configs.

		# Replace old values with new inputs
		# Shadow settings
		for item, value in settings2file.items():
			string_start = r"^%s =(.*);" % item
			if re.search(string_start,old_config,re.MULTILINE):
				old_config = re.sub(string_start, r"%(item)s = %(value)s;" % {"item":item, "value":str(value)}, old_config,flags=re.MULTILINE)
			else:
				old_config = old_config + "%(item)s = %(value)s;\n" % {"item":item, "value":str(value)}
			
		# Fix uppercase
		old_config = re.sub("False","false",old_config)
		old_config = re.sub("True","true",old_config)

		# Float fix?
		old_config = re.sub("00000","",old_config)
		
		# Debug
		#print old_config

		# Write new configuration file
		with open(COMPTON, "w+") as f:
			f.write(old_config)

		# Restart compton
		self.thread_killcompton()
		self.main.destroy()

		# close Paranoid
		Gtk.main_quit()

if __name__ == "__main__":

	import signal
	signal.signal(signal.SIGINT, signal.SIG_DFL)

	if not os.path.isfile(COMPTON):
		
		with open(COMPTON, "w+") as f:
			f.write("# compton.conf generated by paranoid\n")
		newconf = True

	g = GUI()
	Gtk.main()

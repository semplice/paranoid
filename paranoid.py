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
import gobject
#import os
import re
import string

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

			# Return float value
			# Many values like menu-opacity are float 
			return float(result)

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

		# Get Settings window
		self.settings = self.builder.get_object("settings")
		
		#### Main window
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

		# Exit button
		#self.exit = self.builder.get_object("exit")
		#self.exit.connect("clicked", Gtk.main_quit)

		# Save & apply button
		self.save = self.builder.get_object("save")
		self.save.connect("clicked", self.save_apply)

		# Settings button
		self.settings_button = self.builder.get_object("settings_button")
		self.settings_button.connect("clicked", self.show_settings)

		#### Settings window
		# Enable desktop effects checkbox
		self.enable_effects = self.builder.get_object("enable-desktop-effects")

		# Close button
		self.cancel_settings = self.builder.get_object("cancel-settings")
		self.cancel_settings.connect("clicked", self.close_settings)

		# Save & apply button
		self.save_settings = self.builder.get_object("save-settings")
		#self.save_settings.connect("clicked", self.save_settings)

		# Show it
		if self.shadow.get_active() == False:
			self.shadow_box.set_sensitive(False)
		if self.fading.get_active() == False:
			self.fading_box.set_sensitive(False)
		if not donotshow: self.main.show_all()


	def save_settings(self, obj, opt = None):
		""" Save settings """

	def show_settings(self, obj, opt = None):
		# Show settings window
		self.settings.show_all()

	def close_settings(self, obj, opt = None):
		# Close settings window
		self.settings.destroy()

	def fading_switch(self, obj, opt = None):
		# Switch Fading on/off
		self.fading_box.set_sensitive(invertbool(self.fading.get_active()))

	def shadow_switch(self, obj, opt = None):
		# Switch Shadow on/off
		self.shadow_box.set_sensitive(invertbool(self.shadow.get_active()))

	def save_apply(self, obj):
		# Save & apply click event
		# this should write the new configuration into compton.conf
		# Open and read old configuration file
		old_config_file = open(COMPTON,'r')
		old_config = old_config_file.read()
		old_config_file.close()

		# Replace old values with new inputs
		# Shadow settings
		old_config = (re.sub("shadow =(.*);", "shadow = %r;" % self.shadow.get_active(), old_config))
		old_config = (re.sub("no-dock-shadow =(.*);", "no-dock-shadow = %r;" % invertbool(self.panel_shadow.get_active()), old_config))
		old_config = (re.sub("clear-shadow =(.*);", "clear-shadow = %r;" % self.clear_shadow.get_active(), old_config))
		old_config = (re.sub("shadow-radius =(.*);", "shadow-radius = %d;" % self.radius.get_value(), old_config))
		
		# Fading settings
		old_config = (re.sub("fading =(.*);", "fading = %r;" % self.fading.get_active(), old_config))
		old_config = (re.sub("no-fading-openclose =(.*);", "no-fading-openclose = %r;" % invertbool(self.fading_openclose.get_active()), old_config))
		old_config = (re.sub("fade-delta =(.*);", "fade-delta = %f;" % (self.fade_delta.get_value()), old_config))

		# Opacity settings
		old_config = (re.sub("menu-opacity =(.*);", "menu-opacity = %f;" % (self.menu_opacity.get_value()/10), old_config))
		old_config = (re.sub("inactive-opacity =(.*);", "inactive-opacity = %f;" % (self.inactive_opacity.get_value()/10 ),old_config))
		old_config = (re.sub("frame-opacity =(.*);", "frame-opacity = %f;" % (self.frame_opacity.get_value()/10 ),old_config))

		# Others settings
		old_config = (re.sub("inactive-opacity-override =(.*);", "inactive-opacity-override = %r;" % self.inactive_opacity_override.get_active(), old_config))
		old_config = (re.sub("shadow-ignore-shaped =(.*);", "shadow-ignore-shaped = %r;" % self.shadow_ignore_shaped.get_active(), old_config))
		old_config = (re.sub("mark-wmwin-focused =(.*);", "mark-wmwin-focused = %r;" % self.mark_wmwin_focused.get_active(), old_config))
		old_config = (re.sub("blur-background-fixed =(.*);", "blur-background-fixed = %r;" % self.blur_background_fixed.get_active(), old_config))
		old_config = (re.sub("detect-rounded-corners =(.*);", "detect-rounded-corners = %r;" % self.detect_rounded_corners.get_active(), old_config))

		# Fix uppercase
		old_config = (re.sub("False","false",old_config))
		old_config = (re.sub("True","true",old_config))

		# Float fix?
		old_config = (re.sub("00000","",old_config))

		# Debug
		#print old_config

		# Write new configuration file
		new_config_file = open(COMPTON,'w')
		new_config_file.write(old_config)
		new_config_file.close()
		
		Gtk.main_quit()

if __name__ == "__main__":
	g = GUI()
	Gtk.main()

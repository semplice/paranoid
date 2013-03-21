#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Paranoid - setup.py
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

from distutils.core import setup

setup(name='paranoid',
      version='1.0.3',
      description='GTK+3 configuration tool for compton.',
      author='Giuseppe Corti and the Semplice Team',
      author_email='gsc.rul3z@gmail.com',
      url='https://github.com/semplice/paranoid',
     # package_dir={'bin':''},
      scripts=['paranoid.py'],
      data_files=[("/usr/share/paranoid", ["paranoid.glade"])],
      requires=['gi.repository.Gtk', 'gobject', 'threading.Thread', 'os', 're', 'string'],
     )

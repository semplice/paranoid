#!/bin/bash

#
# Simple script that creates .mo for every .po found in lang/template
# Copyright (C) 2011 Eugenio "g7" Paolantonio. All rights reserved.
# Work released under the GNU GPL License, version 3 or later.
#

APP_NAME="paranoid"

cd ./lang/$APP_NAME

for name in `find . -name "*.po"`; do
	lang=${name/".po"/""}
	msgfmt --output-file=$lang.mo $name
done

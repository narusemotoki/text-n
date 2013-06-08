#!/bin/sh
: <<'#__COMMENT_OUT__'
text-n
Copyright (C) 2013 Motoki Naruse <motoki@naru.se>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
#__COMMENT_OUT__
if [ ! -e google_appengine ]; then
  wget http://googleappengine.googlecode.com/files/google_appengine_1.8.0.zip
  unzip -q google_appengine_1.8.0.zip
  rm google_appengine_1.8.0.zip
fi

if [ ! `which grunt` ]; then
  sudo env PATH=$PATH npm install -g -q grunt-cli
fi


if [ ! `which karma` ]; then
  sudo env PATH=$PATH npm install -g -q karma
fi

if [ ! `which phantomjs` ]; then
  sudo env PATH=$PATH npm install -g -q phantomjs
fi

npm install

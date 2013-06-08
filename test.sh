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
./setup.sh

PEP8RESULT=`pep8 . --exclude=google_appengine 2>&1`
if [ -n "$PEP8RESULT" ]; then
  echo $PEP8RESULT
else
  echo PEP8 OK
fi

nosetests test/appengine -s

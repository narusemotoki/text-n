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
  ZIP_NAME='google_appengine_1.8.3.zip'
  wget http://googleappengine.googlecode.com/files/$ZIP_NAME
  unzip -q $ZIP_NAME
  rm $ZIP_NAME
fi

if [ ! -e appengine/fonts ]; then
  wget 'http://sourceforge.jp/frs/redir.php?m=jaist&f=%2Fvlgothic%2F58961%2FVLGothic-20130607.zip' -O font.zip
  unzip -q font.zip
  rm font.zip
  mv -f VLGothic appengine/fonts
fi

# Download JavaScript libraries
wget http://code.angularjs.org/1.1.5/angular.min.js
mkdir -p appengine/static/js
mv angular.min.js appengine/static/js/.
wget http://code.angularjs.org/1.1.5/angular-mocks.js
mkdir -p test
mv angular-mocks.js test/.

# Download CSS libraries
wget https://github.com/twbs/bootstrap/archive/v3.0.0.zip
unzip -q v3.0.0.zip
mkdir -p appengine/static/css
mv bootstrap-3.0.0/dist/css/bootstrap.min.css appengine/static/css/.
rm -rf bootstrap-3.0.0 v3.0.0.zip

# Download google-code-prettify
wget http://google-code-prettify.googlecode.com/files/prettify-small-4-Mar-2013.tar.bz2
tar -xf prettify-small-4-Mar-2013.tar.bz2
mv google-code-prettify/prettify.js appengine/static/js/.
mv google-code-prettify/prettify.css appengine/static/css/.
rm -rf google-code-prettify prettify-small-4-Mar-2013.tar.bz2

npm install
if [ ! `which grunt` ]; then
  sudo env PATH=$PATH npm install -g -q grunt-cli
fi

if [ ! `which karma` ]; then
  sudo env PATH=$PATH npm install -g -q karma
fi

if [ ! `which phantomjs` ]; then
  sudo env PATH=$PATH npm install -g -q phantomjs
fi

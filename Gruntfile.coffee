###
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
###
module.exports = (grunt) =>
  pkg = grunt.file.readJSON 'package.json'
  grunt.initConfig
    coffee:
      main:
        src: ['coffee/**/*.coffee']
        dest: 'appengine/static/js/textn.js'
      test:
        src: ['test/coffee/**/*.coffee']
        dest: 'test/test.js'
    clean:
      main:
        src: ['<%= coffee.main.dest %>', '<%= coffee.test.dest %>']
    watch:
      files: ['<%= coffee.main.src %>', '<%= coffee.test.dest %>']
      tasks: ['test']
    karma:
      unit:
        configFile: 'karma.conf.js'
        browsers: ['PhantomJS']
        autoWatch: false
        reporters: ['progress', 'junit']
        singleRun: true
        keepalive: true
        color: true

  grunt.registerTask 'default', ['clean','coffee']
  grunt.registerTask 'test', ['default', 'karma']
  grunt.loadNpmTasks 'grunt-contrib-coffee'
  grunt.loadNpmTasks 'grunt-contrib-clean'
  grunt.loadNpmTasks 'grunt-contrib-watch'
  grunt.loadNpmTasks 'grunt-karma'
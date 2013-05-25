module.exports = (grunt) => grunt.initConfig
  coffee:
    main:
      src: ['coffee/**/*.coffee']
      dest: 'appengine/static/js/textn.js'
  clean:
    main:
      src: '<%= coffee.main.dest %>'
  watch:
    files: ['<%= coffee.main.src %>']
    tasks: ['default']

  grunt.registerTask 'default', ['clean','coffee']
  grunt.loadNpmTasks 'grunt-contrib-coffee'
  grunt.loadNpmTasks 'grunt-contrib-clean'
  grunt.loadNpmTasks 'grunt-contrib-watch'
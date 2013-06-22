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

angular.module('textn', []).config ($routeProvider) =>
  $routeProvider.when '/html/:key',
    templateUrl: 'static/partial/html.html'
    controller: 'HtmlCtrl'
  .when '/mine',
    templateUrl: 'static/partial/mine.html'
    controller: 'MineCtrl'
  .otherwise
    templateUrl: 'static/partial/edit.html'
    controller: 'EditCtrl'
.service 'url', ($rootScope) =>
  baseUrl = $rootScope.baseUrl

  createPlainText: (key) => baseUrl + '/plaintext/' + key
  createImageText: (key) => baseUrl + '/api/imagetext/' + key + '.png'
  createHtml: (key) => baseUrl + '/#/html/' + key
.run ($rootScope, $location, $window) =>
  $rootScope.appName = 'text-n'
  $rootScope.baseUrl = $location.protocol() + '://' +
    $location.host() +
    unless $location.port() in [80, 443]
      ':' + $location.port()
    else
      ''
  $rootScope.commonErrorHandle = (data, status) =>
    if status is 401
      escapedPath = $window.escape '#' + $location.path()
      $window.location.href = $rootScope.baseUrl + '/auth/login/' + escapedPath
.filter 'nl2br', => (source) =>
  String(source).replace /\r?\n/g, '<br />' if source

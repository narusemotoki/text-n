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

@HtmlCtrl = ($scope, $routeParams, $http, url) =>
  TEXT_PATH = 'api/text'

  $scope.plainTextUrl = url.createPlainText $routeParams.key
  $scope.imageTextUrl = url.createImageText $routeParams.key
  $scope.htmlUrl = url.createHtml $routeParams.key

  $scope.isLoading = true
  $http.get(TEXT_PATH + '/' + $routeParams.key)
  .success (data) =>
    $scope.text = data
    $scope.isLoading = false
  .error (data, status) => $scope.commonErrorHandle data, status

  $scope.switchPrettyprint = =>
    $scope.isEnabledSyntaxHighlighting = !$scope.isEnabledSyntaxHighlighting
    prettyPrint() if $scope.isEnabledSyntaxHighlighting

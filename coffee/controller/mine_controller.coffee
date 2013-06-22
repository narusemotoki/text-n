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
@MineCtrl = ($scope, $http, url) =>
  MINE_PATH = 'api/mine'

  $scope.createUrl = (text) => url.createHtml text.key

  $scope.isLoading = true
  $http.get(MINE_PATH)
  .success (data) =>
    $scope.texts = data
    $scope.isLoading = false
  .error (data, status) => $scope.commonErrorHandle data, status

  $scope.introduce = (text) => text.text.match(/(.*\n?){1,5}/)[0]

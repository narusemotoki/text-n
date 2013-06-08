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

@EditCtrl = ($scope, $http, $location) =>
  TEXT_PATH = 'api/text'

  $scope.add = =>
    $scope.approvals.push approval: $scope.approval
    $scope.approval = ''

  $scope.submit = =>
    data =
      text: $scope.text
      approvals: []
      password: $scope.password
    data.approvals.push a.approval for a in $scope.approvals

    $http.post(TEXT_PATH, data)
    .success (data) => $location.path('/html/' + data.key)

  $scope.delete = (index) => $scope.approvals.splice(index, 1)

  $scope.isLoading = true
  $http.get(TEXT_PATH)
  .success (data) =>
    $scope.user = data.user
    $scope.approvals = []
    unless data.user.match(/@gmail.com$/)
      $scope.approvals.push
        approval: data.user.substr (data.user.lastIndexOf '@') + 1
    $scope.isLoading = false
  .error (data, status) => $scope.commonErrorHandle data, status

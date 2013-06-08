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
describe 'EditCtrl', =>
  module 'textn'
  beforeEach inject (@$controller, $rootScope, @$httpBackend) =>
    @$scope = $rootScope.$new()

  describe 'initialize', =>
    it 'logged in with Gmail', =>
      email = 'test@gmail.com'

      $httpBackend.expectGET('api/text')
      .respond
        user: email

      $controller EditCtrl, $scope: $scope

      $httpBackend.flush()

      expect($scope.user).toEqual email
      expect($scope.approvals.length).toEqual 0

    it 'logged in with Google Apps', =>
      email = 'test@googleapps.com'

      $httpBackend.expectGET('api/text')
      .respond
        user: email

      $controller EditCtrl, $scope: $scope

      $httpBackend.flush()

      expect($scope.user).toEqual email
      expect($scope.approvals.length).toEqual 1
      expect($scope.approvals[0]).toEqual approval: 'googleapps.com'

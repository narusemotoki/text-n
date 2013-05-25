@ResultCtrl = ($scope, $routeParams, $location) =>
  $scope.result = $scope.baseUrl + '/planetext/' + $routeParams.key

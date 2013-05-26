@HtmlCtrl = ($scope, $routeParams, $http) =>
  TEXT_PATH = 'api/text'

  $scope.planeTextUrl = $scope.baseUrl + '/planetext/' + $routeParams.key
  $scope.htmlUrl = $scope.baseUrl + '/#/html/' + $routeParams.key

  $scope.isLoading = true
  $http.get(TEXT_PATH + '/' + $routeParams.key)
  .success (data) =>
    $scope.text = data
    $scope.isLoading = false

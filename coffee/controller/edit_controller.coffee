@EditCtrl = ($scope, $http, $location) =>
  TEXT_PATH = 'api/text'

  $http.get(TEXT_PATH)
  .success (data) =>
    $scope.user = data.user
    $scope.approvals = [data.user]

  $scope.submit = =>
    data =
      text: $scope.text
      approvals: $scope.approvals
      password: $scope.password

    $http.post(TEXT_PATH, data)
    .success (data) => $location.path('/result/' + data.key)

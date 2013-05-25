@EditCtrl = ($scope, $http, $location) =>
  TEXT_PATH = 'api/text'

  $scope.add = =>
    $scope.approvals.push approval: $scope.approval
    $scope.approval = ''

  $http.get(TEXT_PATH)
  .success (data) =>
    $scope.user = data.user
    $scope.approvals = []
    unless data.user.match(/@gmail.com$/)
      $scope.approvals.push
        approval: data.user.substr (data.user.lastIndexOf '@') + 1

  $scope.submit = =>
    data =
      text: $scope.text
      approvals: $scope.approvals
      password: $scope.password

    $http.post(TEXT_PATH, data)
    .success (data) => $location.path('/result/' + data.key)

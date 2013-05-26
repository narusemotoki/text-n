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

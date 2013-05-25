angular.module('textn', []).config ($routeProvider) =>
  $routeProvider.when '/result/:key',
    templateUrl: 'static/partial/result.html'
    controller: 'ResultCtrl'
  .otherwise
    templateUrl: 'static/partial/edit.html'
    controller: 'EditCtrl'
.run ($rootScope,  $location) =>
  $rootScope.baseUrl = $location.protocol() + '://' +
    $location.host() +
    unless $location.port() in [80, 443]
      ':' + $location.port()
    else
      ''
.filter 'nl2br', => (source) =>
  String(source).replace /\r?\n/g, '<br />' if source

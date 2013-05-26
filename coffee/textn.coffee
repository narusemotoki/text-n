angular.module('textn', []).config ($routeProvider) =>
  $routeProvider.when '/html/:key',
    templateUrl: 'static/partial/html.html'
    controller: 'HtmlCtrl'
  .otherwise
    templateUrl: 'static/partial/edit.html'
    controller: 'EditCtrl'
.run ($rootScope,  $location) =>
  $rootScope.appName = 'text-n'
  $rootScope.baseUrl = $location.protocol() + '://' +
    $location.host() +
    unless $location.port() in [80, 443]
      ':' + $location.port()
    else
      ''
.filter 'nl2br', => (source) =>
  String(source).replace /\r?\n/g, '<br />' if source

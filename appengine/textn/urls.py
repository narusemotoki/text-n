from django.conf.urls.defaults import patterns

urlpatterns = patterns(
    'textn.views',
    (r'^(?P<message>.*)$', 'index'),
)

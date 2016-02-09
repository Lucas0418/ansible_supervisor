from django.conf.urls import url
from . import views

app_name = 'inventory'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<host_id>[0-9]+)/detail/$', views.detail, name='detail'),
    url(r'^(?P<host_id>[0-9]+)/change/$', views.change, name='change'),
    url(r'^(?P<host_id>[0-9]+)/testchange/$', views.testchange, name='testchange'),
    url(r'^(?P<host_id>[0-9]+)/results/$', views.results, name='results'),
]

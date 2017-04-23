from django.conf.urls import url

from . import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^backend/$', views.backend_list),
    url(r'^backend/(?P<pk>[0-9]+)/$', views.backend_detail),
]

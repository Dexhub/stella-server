from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    #url(r'^backend/$', views.backend_list),
    url(r'^restaurant/$', views.get_restaurant_list),
    url(r'^menu_info/$', views.get_menu_info),
    #:url(r'^backend/(?P<pk>[0-9]+)/$', views.backend_detail),
]

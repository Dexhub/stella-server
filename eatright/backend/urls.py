from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^restaurant/$', views.get_restaurant_list),
    url(r'^menu_info/$', views.get_menu_info),
]

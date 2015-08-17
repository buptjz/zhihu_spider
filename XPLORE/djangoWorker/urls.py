from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^check_proxy$', views.check_proxy, name='check_proxy'),
]
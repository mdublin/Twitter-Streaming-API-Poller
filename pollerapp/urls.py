from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^twitter-api/', views.twitter_api, name='twitter_api'),
]


from django.conf.urls import patterns, url

from stamped import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'results/', views.results, name='results'),
    url(r'feed/', views.feed_home, name='feed'),
)
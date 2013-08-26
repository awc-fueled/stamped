from django.conf.urls import patterns, url
from stamped import views
from stamped_project import settings

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^results/', views.results, name='results'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}),
    url(r'^upload_file/', views.upload_file, name='upload_file'),
    url(r'^add_comment/', views.make_comment, name='make_comment'),    
    url(r'^create_user/', views.create_user, name='create_user'),
    url(r'^create_user_meta/', views.create_user_meta, name='create_user_meta'),
)
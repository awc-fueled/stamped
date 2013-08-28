from django.conf.urls import patterns, url
from stamped import views
from stamped_project import settings

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^results/', views.results, name='results'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}),
    url(r'^add_comment/', views.add_comment, name='add_comment'),
    url(r'^add_review/', views.add_review, name='add_review'),  
    url(r'^stamp_out/', views.stamp_out, name='stamp_out'),   
    url(r'^create_user/', views.create_user, name='create_user'),
    url(r'^create_user_meta/', views.create_user_meta, name='create_user_meta'),
    url(r'^without_permission/', views.without_permission, name='without_permission'),
)
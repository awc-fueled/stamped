from django.conf.urls import patterns, url
from stamped import views
from stamped_project import settings

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^results/', views.results, name='results'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}),
    url(r'^upload_file/', views.upload_file), ## might not need this view becuase form is now inline
    url(r'^custom_tag/', views.custom_tag),
    url(r'^add_comment/', views.make_comment),
)
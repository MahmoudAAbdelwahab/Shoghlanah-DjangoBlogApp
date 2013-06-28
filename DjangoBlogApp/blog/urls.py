from django.conf.urls import patterns, url

from blog import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^create/$', views.create_blog, name='create_blog'),
	url(r'^(?P<blog_id>\d+)/$', views.show_blog, name='show_blog'),
    url(r'^(?P<blog_id>\d+)/delete/$', views.delete_blog, name='delete_blog'),
    
    url(r'^login/$', views.login_user, name='login'),
	url(r'^logout/$', views.logout_user, name='logout'),

    url(r'^(?P<blog_id>\d+)/post/create/$', views.create_post, name='create_post'),
	url(r'^post/(?P<post_id>\d+)/$', views.show_post, name='show_post'),
    url(r'^post/(?P<post_id>\d+)/delete/$', views.delete_post, name='delete_post'),
    url(r'^post/(?P<post_id>\d+)/comment/add/$', views.add_comment, name='add_comment')
)
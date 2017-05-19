from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^register/$', views.register, name='register'),
    url(r'^loginresult/$', views.loginresult, name='loginresult'),
   	url(r'^forgotpass/$', views.forgotpass, name='forgotpass'),
    url(r'^log_out/$', views.log_out, name='log_out'),
    url(r'^newpassword/$', views.newpassword, name='newpassword'),
    url(r'^recover_password/$', views.recover_password, name='recover_password'),
    url(r'^create_blog/$',views.create_blog,name='create_blog'),
    url(r'^manage_blog/$',views.manage_blog,name='manage_blog'),
    url(r'^delete_blog/$',views.delete_blog,name='delete_blog'),
    url(r'^update_blog/(?P<id>\d+)/$',views.update_blog,name='update_blog'),
    url(r'^update_delete_blog/$',views.update_delete_blog,name='update_delete_blog'),
    url(r'^detail_blog/(?P<id>\d+)/$',views.detail_blog,name='detail_blog'),
]

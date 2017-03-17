from django.conf.urls import url
from . import views


urlpatterns=[
	url(r'^$', views.home,name='home'),
	url(r'^forgotpass/$', views.forgotpass,name='forgotpass'),
	url(r'^adminlogin/$', views.adminlogin,name='forgotpass'),
	url(r'^resetpassword/$', views.resetpassword,name='resetpassword'),
	url(r'^registration/$', views.registration,name='registration'),
]






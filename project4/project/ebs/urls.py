from django.conf.urls import url
from . import views

urlpatterns=[
	url(r'^$', views.home,name="home"),
	url(r'^forgotpass/$', views.forgotpass,name='forgotpass'),
	url(r'^adminlogin/$', views.adminlogin,name='adminlogin'),
	url(r'^resetpassword/$', views.resetpassword,name='resetpassword'),
	url(r'^regresult/$', views.regresult,name='regresult'),
	url(r'^registration/$', views.registration,name='registration'),
	url(r'^loginresult/$', views.loginresult,name='loginresult'),
	url(r'^forgotpassword/$', views.forgotpassword,name='forgotpassword'),
	url(r'^log_out/$', views.log_out,name='log_out'),
]

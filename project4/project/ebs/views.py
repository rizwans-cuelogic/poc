import json
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import Organisation,forgotpassword
from .forms import UserForm,OrgForm,UserLoginForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import (authenticate,login,logout,)
from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string, get_template
import sys
from datetime import datetime, timedelta
import hashlib
import os
import uuid
from django.utils.html import strip_tags
# Create your views here.

def home(request):
	f1=UserForm()
	f2=OrgForm()
	f3=UserLoginForm()
	return render(request,'ebs/home.html',{'f1':f1,'f2':f2,'f3':f3})

def adminlogin(request):
	return render(request,'ebs/adminlogin.html')

def forgotpass(request):
	return render(request,'ebs/forgotpass.html')

def resetpassword(request):
	return render(request,'ebs/newpassword.html')

def registration(request):
	return render(request,'ebs/Registration.html')


def regresult(request):
	"""Views for registering client to plateform take UserForm and OrgForm save it to User object
	and organisation object"""
	if request.method=='POST':
		f1=UserForm(request.POST or None,request.FILES or None)
		f2=OrgForm(request.POST or None,request.FILES or None )
		if f1.is_valid() and f2.is_valid():
		 	user = User.objects.create_user(f1.cleaned_data['username'], f1.cleaned_data['email'], f1.cleaned_data['password'],is_active='False')
		 	organisation=f2.save(commit=False)
		 	organisation.user=user
		 	g = Group.objects.get(name='client') 
		 	g.user_set.add(user)
		 	organisation.save()
		 	user.save()
		 	response = {'status':'success', 'message': 'Your account has been created and pending for admin approval.  You will get an email after admin approval on your registered email id. This process will take 24 hours.'}
			return HttpResponse(json.dumps(response), content_type='application/json')
	
		else:
			error=json.dumps(f1.errors)
			errorstring=json.loads(error)
			if 'username' in errorstring and errorstring['username']==[u'username already exists']:
				response = {'status':'Error', 'message': "username already exists"}
			elif 'email' in errorstring and errorstring['email']==[u'Email already exists']:	
		 		response = {'status':'Error', 'message': "email already exists"}	
			else:
				response = {'status':'Error', 'message': "please fill the details"}
			
			return HttpResponse(json.dumps(response), content_type='application/json')
	else:
	 	f1=UserForm();
	 	f2=OrgForm();
	 	f3=UserLoginForm()
	 	return render(request,'ebs/home.html',{'f1':f1,'f2':f2,'f3':f3})

def loginresult(request):
	f1=UserForm()
	f2=OrgForm()
	f3=UserLoginForm()
	if request.method=='POST':
		f3=UserLoginForm(request.POST or None)
		if f3.is_valid():
			username=f3.cleaned_data['username']
			password = f3.cleaned_data['password']
			user=authenticate(username=username,password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					response = {'status':'success', 'message': "good", "user":user.username}
					return HttpResponse(json.dumps(response), content_type='application/json')				
				else:
					response = {'status':'Error', 'message': "User is inactive try again"}
			else:
				response = {'status':'Error', 'message': "Invalid Username and Password"}
			return HttpResponse(json.dumps(response), content_type='application/json')

def log_out(request):
	logout(request)
	f1=UserForm()
	f2=OrgForm()
	f3=UserLoginForm()
	return HttpResponseRedirect('/')

def forgotpassword(request):
	try:
		if request.method=='POST':
			"""import pdb
			pdb.set_trace()"""
			data = json.loads(request.body)
			email=data['email']
			user=User.objects.get(email=email)
			if user.is_active:
				hash1 = str(uuid.uuid1())
				obj=user.forgotpassword_set.create(activation_key=hash1,link_time=datetime.now())
				subject = 'Password recovery'
				html_content=render_to_string('ebs/mail.html', {'hash1':hash1,'HOST':settings.HOST,'user':user})
				text_content=strip_tags(html_content) 
				from_email = settings.EMAIL_HOST_USER
				msg = EmailMultiAlternatives(subject, text_content, from_email, [user.email])	
				msg.attach_alternative(html_content, "text/html")
				msg.send()
				response = {'status':'success', 'message': "Reset password link has been email to your registered email address."}
				return HttpResponse(json.dumps(response), content_type='application/json')
			else:
				response = {'status':'Error', 'message': "Invalid email"}
				return HttpResponse(json.dumps(response), content_type='application/json')

	except Exception as e:
		print e
		response = {'status':'Error', 'message': "Invalid email"}
		return HttpResponse(json.dumps(response), content_type='application/json')

def forgotpass_link(request):
	hash1=request.GET.get('uid', '')
	if (hash1):
		obj=forgotpassword.objects.get(activation_key=hash1)
		user=User.objects.get(username=obj.username)	
		time_date=obj.link_time        
		if time_date < (datetime.now() - timedelta(hours=48)):
			raise ValidationError('link has been expired')
		else:
			raise ValueError('Wrong hashkey')


    
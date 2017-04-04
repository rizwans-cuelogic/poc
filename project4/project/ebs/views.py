from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.models import Group
from django import forms
from django.forms import ModelForm
from django.http import HttpResponse
from .forms import UserForm,OrgForm
from django.shortcuts import render
import json
from .models import Organisation
import sys
# Create your views here.

def home(request):
	userform=UserForm();
	orgform=OrgForm();
	return render(request,'ebs/home.html',{'userform':userform,'orgform':orgform})

def register(request):
	"""Client Registration: View hich take UserForm and OrgForm save it to User object
	and organisation object"""
	if request.method=='POST':
		userform=UserForm(request.POST or None,request.FILES or None)
		orgform=OrgForm(request.POST or None,request.FILES or None )
		if userform.is_valid() and orgform.is_valid():
		 	user = User.objects.create_user(userform.cleaned_data['username'], 
		 	userform.cleaned_data['email'], userform.cleaned_data['password'],is_active='False')
		 	organisation=orgform.save(commit=False)
		 	organisation.user=user
		 	g = Group.objects.get(name='client') 
		 	g.user_set.add(user)
		 	organisation.save()
		 	user.save()
		 	response = {'status':'success', 
		 		'message': ('Your account has been created and pending for admin approval.' 
		 		'You will get an email after admin approval on your registered email id. This process will take 24 hours.')}
			return HttpResponse(json.dumps(response), content_type='application/json')
	
		else:
			error=json.dumps(userform.errors)
			errorstring=json.loads(error)
			if 'username' in errorstring and errorstring[
					'username']==[u'username already exists']:
				response = {
					'status':'Error', 
					'message': "username already exists"
				}
			elif 'email' in errorstring and errorstring[
					'email']==[u'Email already exists']:	
		 		response = {'status':'Error', 'message': "email already exists"}	
			else:
				response = {
					'status':'Error', 
					'message': "please fill the details"
				}
			return HttpResponse(json.dumps(response), content_type='application/json')
	else:
	 	userform=UserForm();
	 	orgform=OrgForm();
	 	return render(request,'ebs/home.html',{'userform':userform,'orgform':orgform})
	 

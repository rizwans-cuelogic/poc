from django.shortcuts import render
from django.http import HttpResponse
from .models import Organisation
from .forms import UserForm,OrgForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib import messages
from django.contrib.auth.models import Group
# Create your views here.

def home(request):
	f1=UserForm();
	f2=OrgForm();
	return render(request,'ebs/home.html',{'f1':f1,'f2':f2})

def adminlogin(request):
	return render(request,'ebs/adminlogin.html')

def forgotpass(request):
	return render(request,'ebs/forgotpass.html')

def resetpassword(request):
	return render(request,'ebs/newpassword.html')

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

			messages.info(request,"Your account has been created and pending for admin approval.  You will get an email after admin approval on your registered email id. This process will take 24 hours.")			
			return render(request,'ebs/home.html',{'f1':f1,'f2':f2})	

		else:
			return render(request,'ebs/home.html',{'f1':f1,'f2':f2})	
	else:
		f1=UserForm();
		f2=OrgForm();
		return render(request,'ebs/home.html',{'f1':f1,'f2':f2})
	
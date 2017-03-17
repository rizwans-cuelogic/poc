from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def home(request):
	return render(request,'plateform/home.html')


def adminlogin(request):
	return render(request,'plateform/adminlogin.html')

def forgotpass(request):
	return render(request,'plateform/forgotpass.html')


def resetpassword(request):
	return render(request,'plateform/newpassword.html')

def registration(request):
	return render(request,'plateform/Registration.html')

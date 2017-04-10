import unittest
import os
import json

from django.test import TestCase,Client
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.utils import setup_test_environment

from . import views
from .models import Organisation
from .forms import UserForm,OrgForm,UserLoginForm

# Create your tests here.
class Test1(TestCase):
	def create_user(self):
		user=User.objects.create(username='asd1234',email='rizwan.shaikh@cuelogic.com',password='As123456')
		return user
	"""def create_user(self, orgname="Anything"):
		user=User.objects.create(username="abcdsadd ",password="As123456sds")
		return Organisation.objects.create(user=user,orgname="Anything")
	
	def test_Organisation(self):
		w = self.create_user()
		self.assertTrue(isinstance(w, Organisation))
		self.assertEqual(w.__unicode__(), 'Organisation :'+w.orgname)


	def test_valid_form(self):
		data = {'username': 'Abcd1234','email':'abc@gmail.com','password': 'As123456','password1':'As123456'}
		form = UserForm(data=data)
		self.assertTrue(form.is_valid())

	def test_invalid_form(self):
		w =User.objects.create(username='Foo', password='')
		data = {'username': w.username, 'password': w.password,}
		form = UserForm(data=data)
		self.assertFalse(form.is_valid())

	def test_valid_login_form(self):
		data={'username':'abcd1234','password':'As123456'}
		form=UserLoginForm(data=data)
		self.assertTrue(form.is_valid())
	
	def test_register(self):
		client=Client()
		response=client.post(reverse('register'),{'username':'abc123','email':'abc@gmail.com','password':'As123456','orgname':'Uvitransform'})
		self.assertTrue(response.status_code,200)
	"""
	
	def test_login(self):
		w=self.create_user()
		client=Client()
		response=client.post(reverse('loginresult'),{'username':'asd1234','password':'As123456'})
		print response.content
		self.assertTrue(response.status_code,200)
		#self.assertContains(response,'{"status": "success", "message": "good", "user": "asd1234"}')

	def test_forgotpass(self):
		w=self.create_user()
		client=Client()
		email={'email':'rizwan.shaikh@cuelogic.com'}
		response=client.post(reverse('forgotpass'),json.dumps(email),content_type="application/json")
		self.assertTrue(response.status_code,200)
		self.assertContains(response,'{"status": "success", "message": "Reset password link has been email to your registered email address."}'
)

	def test_forgotpass2(self):
		w=self.create_user()
		client=Client()
		email={'email':'rizwan.shaikh@gmail.com'}
		response=client.post(reverse('forgotpass'),json.dumps(email),content_type="application/json")
		self.assertTrue(response.status_code,200)
		self.assertContains(response,'{"status": "Error", "message": "Invalid email"}'
)

import unittest
import os

from django.test import TestCase,Client
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import RequestFactory

from . import views
from .models import Organisation
from .forms import UserForm,OrgForm,UserLoginForm

# Create your tests here.
"""
def setUp(self):

    self.user = UserFactory()
    self.factory = RequestFactory()

"""
class Test1(unittest.TestCase):
		
	def test_whatever_creation(self):
		w = self.create_whatever()
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
	
	def create_whatever(self, orgname="Anything"):
		user=User.objects.create(username="abcdsadd ",password="As123456sds")
		return Organisation.objects.create(user=user,orgname="Anything")

	def test_whatever_list_view(self):
		w = self.create_whatever()
		url = reverse("login")
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 200)
		self.assertIn(w.title, resp.content)



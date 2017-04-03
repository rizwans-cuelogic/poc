from django.test import TestCase
import unittest
import os
from .models import Organisation
from .forms import UserForm
from django.core.mail import send_mail
import re
from django.contrib.auth.models import User
from django.contrib.auth.models import User

# Create your tests here.

class Test1(unittest.TestCase):
	
	def create_whatever(self, orgname="Anything"):
		user=User.objects.create(username="abcd ",password="As123456")
		return Organisation.objects.create(user=user,orgname="Anything")

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


	
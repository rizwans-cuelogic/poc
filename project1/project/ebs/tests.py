from django.test import TestCase
import unittest
import os
from django.core.mail import send_mail
import re
from django.contrib.auth.models import User
import project.settings

# Create your tests here.

class Test1(unittest.TestCase):
	
	def test_password_length(self):
		pass1=os.environ.get('pass1')
		self.assertTrue(len(pass1)>=8 and len(pass1)<=16)
		self.assertFalse(len(pass1)>8 or len(pass1)<16)

	def test_password_check(self):
		REGEX = re.compile('^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[a-zA-z\d]+$')
		password=os.environ.get('pass1')
		self.assertTrue(REGEX.match(password))
	
	def test_equal_password(self):
		pass1=os.environ.get('pass1')
		pass2=os.environ.get('pass2')
		self.assertEqual(pass1,pass2)

	def test_username_length(self):
		string=os.environ.get('user')
		self.assertTrue(len(string)>=6)
		self.assertFalse(len(string)<6)

	def test_email_check(self):
		REGEX = re.compile('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
		email=os.environ.get('email')
		self.assertTrue(REGEX.match(email))




	

	


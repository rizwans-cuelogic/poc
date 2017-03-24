from django.test import TestCase
import unittest
import django.auth.models import User
# Create your tests here.

class Test1(Testcase):
	def equal_password(self):
		pass1="As123456"
		pass2="AS123456"
		self.assertFalse(pass1,pass2)
		"""
	def user_object(self):
		user1=User.object.create(username="Rizwan", password="As123456",)

	"""
import unittest
import os
import json
import uuid
from django.contrib.auth.models import Group, Permission
from django.test import TestCase, Client
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.utils import setup_test_environment
from django.utils import timezone
from django.core.files import File
from . import views
from .models import Organisation, forgotpassword
from .forms import UserForm, OrgForm, UserLoginForm

# Create your tests here.


class Test1(TestCase):
	def create_user(self):
		user=User.objects.create(username=os.environ['USERNAME'],email=os.environ['EMAIL_FORGOT'],password=os.environ['EMAIL_FORGOT'])
		return user

	def create_org(self, orgname=os.environ["ORG"]):
		user=User.objects.create(username=os.environ['USERNAME'],password="os.environ['PASSWORD']")
		return Organisation.objects.create(user=user,orgname=os.environ['ORG'])
	
	def test_Organisation(self):
		w = self.create_org()
		self.assertTrue(isinstance(w, Organisation))
		self.assertEqual(w.__unicode__(), 'Organisation :'+w.orgname)


	def test_valid_User_form(self):
		data = {'username': os.environ['USERNAME'],'email':os.environ['EMAIL'],'password': os.environ['PASSWORD'],'password1':os.environ['PASSWORD']}
		form = UserForm(data=data)
		self.assertTrue(form.is_valid())

	def test_invalid_User_form(self):
		w =User.objects.create(username=os.environ['USERNAME'], password='')
		data = {'username': w.username, 'password': w.password,}
		form = UserForm(data=data)
		self.assertFalse(form.is_valid())

	def test_valid_login_form(self):
		data={'username':os.environ['USERNAME'],'password':os.environ['PASSWORD']}
		form=UserLoginForm(data=data)
		self.assertTrue(form.is_valid())

	def test_register(self):
		client = Client()
		img=File(open('/home/rizwan/Downloads/gile.jpg','r'))
		img=str(img)
		new_group,created = Group.objects.get_or_create(name='client')
		response = client.post(reverse('register'), {'username': os.environ['USERNAME'],'email':os.environ['EMAIL'], 'password':os.environ['PASSWORD'],'password1':os.environ['PASSWORD'], 'orgname':os.environ['ORG'], 'orglogo':File(open('/home/rizwan/Downloads/gile.jpg','r'))})
		self.assertTrue(response.status_code, 200)
		self.assertContains(response,'{"status": "success", "message": "Your account has been created and pending for admin approval.  You will get an email after admin approval on your registered email id. This process will take 24 hours."}')

	def test_register_fail(self):
		client = Client()
		new_group,created = Group.objects.get_or_create(name='client')
		response = client.post(reverse('register'), {'username': os.environ['USERNAME'], 'email': os.environ['EMAIL'], 'password': os.environ['PASSWORD'],'password1':os.environ['PASSWORD'], 'orgname': os.environ['ORG'], 'orglogo':'/home/rizwan/Downloads/gile.jpg'})
		self.assertTrue(response.status_code, 200)
		self.assertContains(response,'{"status": "Error", "message": "please fill the details"}')

	def test_login(self):
		user1=User.objects.create(username=os.environ['USERNAME'], email=os.environ['EMAIL'],password=os.environ['PASSWORD'],is_active=True)
		user1.set_password(os.environ['PASSWORD'])
		user1.save()
		client=Client()
		response=client.post(reverse('loginresult'),{'username':os.environ['USERNAME'],'password':os.environ['PASSWORD']})
		self.assertTrue(response.status_code,200)
		self.assertContains(response,'{"status": "success", "message": "good"}')
	
	def test_login_fail(self):
		user1=User.objects.create(username=os.environ['USERNAME'], email=os.environ['EMAIL'],password=os.environ['PASSWORD'],is_active=True)
		client=Client()
		response=client.post(reverse('loginresult'),{'username':os.environ['USERNAME'],'password':os.environ['PASSWORD']})
		self.assertTrue(response.status_code,200)
		self.assertContains(response,'{"status": "Error", "message": "Invalid Username And Password"}')

	def test_forgotpass(self):
		w=self.create_user()
		client=Client()
		email={'email':os.environ['EMAIL_FORGOT']}
		response=client.post(reverse('forgotpass'),json.dumps(email),content_type="application/json")
		self.assertTrue(response.status_code,200)
		self.assertContains(response,'{"status": "success", "message": "Reset password link has been email to your registered email address."}')

	def test_forgotpass_fail(self):
		w=self.create_user()
		client=Client()
		email={'email':os.environ.get('EMAIL')}
		response=client.post(reverse('forgotpass'),json.dumps(email),content_type="application/json")
		self.assertTrue(response.status_code,200)
		self.assertContains(response,'{"status": "Error", "message": "Invalid email"}')
	
	def test_recover_password(self):
		user1=User.objects.create(username=os.environ['USERNAME'], email=os.environ['EMAIL'],password=os.environ['PASSWORD'],is_active=True)
		user1.set_password(os.environ['PASSWORD'])
		user1.save()
		hash1 = str(uuid.uuid1())
		obj=user1.forgotpassword_set.create(activation_key=hash1,link_time=timezone.now())
		client=Client()
		password={'password':os.environ['PASSWORD'],'password1':os.environ['PASSWORD'],'hash':hash1}
		response=client.post(reverse('recover_password'),json.dumps(password),content_type="application/json")
		self.assertTrue(response.status_code,200)
		self.assertContains(response,'{"status": "success", "message": "password updated successfully"}')

	def test_recover_password_fail(self):
		user1=User.objects.create(username=os.environ['USERNAME'], email=os.environ['EMAIL'],password=os.environ['EMAIL_FORGOT'],is_active=True)
		user1.set_password(os.environ['PASSWORD'])
		user1.save()
		hash1 = str(uuid.uuid1())
		obj=user1.forgotpassword_set.create(activation_key=hash1,link_time=timezone.now())
		client=Client()
		hash1='abcdefgh090908hijkl898989898'
		password={'password':os.environ['PASSWORD'],'password1':os.environ['PASSWORD'],'hash':hash1}
		response=client.post(reverse('recover_password'),json.dumps(password),content_type="application/json")
		self.assertTrue(response.status_code,200)
		print response.content
		self.assertContains(response,'{"status": "Error", "message": "invalid link or token has been expired."}')

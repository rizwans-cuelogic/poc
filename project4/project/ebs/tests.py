import unittest
import os
import json
import uuid
from django.contrib.auth.models import Group, Permission
from django.test import TestCase, Client
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.test.utils import setup_test_environment
from django.utils import timezone
from django.core.files import File
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import (authenticate, login, logout,)
from . import views
from .models import Organisation, ForgotPassword,BlogFile,Blog,Comment,Categories
from .forms import UserForm, OrgForm, UserLoginForm,BlogForm,BlogFileForm
# Create your tests here.


class Test1(TestCase):
	def create_user(self):
		user=User.objects.create(username=os.environ['USERNAME'],
								email=os.environ['EMAIL_FORGOT'],
								password=os.environ['EMAIL_FORGOT'])
		return user

	def create_org(self, orgname=os.environ['ORG']):
		user=User.objects.create(username=os.environ['USERNAME'],
								password=os.environ['PASSWORD'])
		return Organisation.objects.create(user=user,orgname=os.environ['ORG'])
	
	def test_Organisation(self):
		w = self.create_org()
		self.assertTrue(isinstance(w, Organisation))
		self.assertEqual(w.__unicode__(),w.orgname)


	def test_valid_User_form(self):
		data = {'username': os.environ['USERNAME'],
				'email':os.environ['EMAIL'],
				'password': os.environ['PASSWORD'],
				'password1':os.environ['PASSWORD']}
		form = UserForm(data=data)
		self.assertTrue(form.is_valid())

	def test_invalid_User_form(self):
		data = {'username':os.environ['USERNAME'], 'password':""}
		form = UserForm(data=data)
		self.assertFalse(form.is_valid())

	def test_valid_login_form(self):
		data={'username':os.environ['USERNAME'],'password':os.environ['PASSWORD']}
		form=UserLoginForm(data=data)
		self.assertTrue(form.is_valid())

	def test_invalid_login_form(self):
		data = {'username': os.environ['USERNAME'], 'password':""}
		form = UserLoginForm(data=data)
		self.assertFalse(form.is_valid())

	def test_register(self):
		client = Client()
		img=File(open('/home/rizwan/a2.jpg','r'))
		img=str(img)
		new_group,created = Group.objects.get_or_create(name='client')
		response = client.post(reverse('register'), 
									{'username': os.environ['USERNAME'],
									'email':os.environ['EMAIL'], 
									'password':os.environ['PASSWORD'],
									'password1':os.environ['PASSWORD'], 
									'orgname':os.environ['ORG'], 
					'orglogo':File(open('/home/rizwan/a2.jpg','r'))
													}
								)
		self.assertTrue(response.status_code, 200)
		self.assertContains(response,'{"status": "success", "message": "Your account has been created and pending for admin approval.  You will get an email after admin approval on your registered email id. This process will take 24 hours."}')

	def test_register_fail(self):
		client = Client()
		new_group,created = Group.objects.get_or_create(name='client')
		response = client.post(reverse('register'),
								 {'username': os.environ['USERNAME'], 
								 'email': os.environ['EMAIL'], 
								 'password': os.environ['PASSWORD'],
								 'password1':os.environ['PASSWORD'],
								 'orgname': os.environ['ORG'],
								 'orglogo':'/home/rizwan/a2.jpg'})
		self.assertTrue(response.status_code, 200)
		self.assertContains(response,'{"status": "Error", "message": "please fill the details"}')

	def test_login(self):
		user1=User.objects.create(username=os.environ['USERNAME'],
		 							email=os.environ['EMAIL'],
		 							password=os.environ['PASSWORD'],
		 							is_active=True)
		user1.set_password(os.environ['PASSWORD'])
		user1.save()
		client=Client()
		response=client.post(reverse('loginresult'),
							{'username':os.environ['USERNAME'],
							'password':os.environ['PASSWORD']})
		self.assertTrue(response.status_code,200)
		self.assertContains(response,'{"status": "success", "message": "good"}')
	
	def test_login_fail(self):
		user1=User.objects.create(username=os.environ['USERNAME'], 
									email=os.environ['EMAIL'],
									password=os.environ['PASSWORD'],
									is_active=True)
		client=Client()
		response=client.post(reverse('loginresult'),
								{'username':os.environ['USERNAME'],
								'password':os.environ['PASSWORD']})
		self.assertTrue(response.status_code,200)
		self.assertContains(response,'{"status": "Error", "message": "Invalid Username And Password"}')

	def test_forgotpass(self):
		w=self.create_user()
		client=Client()
		email={'email':os.environ['EMAIL_FORGOT']}
		response=client.post(reverse('forgotpass'),
						json.dumps(email),content_type="application/json")
		self.assertTrue(response.status_code,200)
		self.assertContains(response,'{"status": "success", "message": "Reset password link has been email to your registered email address."}')

	def test_forgotpass_fail(self):
		w=self.create_user()
		client=Client()
		email={'email':os.environ.get('EMAIL')}
		response=client.post(reverse('forgotpass'),json.dumps(email),
								content_type="application/json")
		self.assertTrue(response.status_code,200)
		self.assertContains(response,'{"status": "Error", "message": "Invalid email"}')
	
	def test_recover_password(self):
		user1=User.objects.create(username=os.environ['USERNAME'],
								 email=os.environ['EMAIL'],
								 password=os.environ['PASSWORD'],
								 is_active=True)
		user1.set_password(os.environ['PASSWORD'])
		user1.save()
		hash1 = str(uuid.uuid1())
		obj=user1.forgotpassword_set.create(activation_key=hash1,
									link_time=timezone.now())
		client=Client()
		password={'password':os.environ['PASSWORD'],
									'password1':os.environ['PASSWORD'],
									'hash':hash1}
		response=client.post(reverse('recover_password'),
									json.dumps(password),
									content_type="application/json")
		self.assertTrue(response.status_code,200)
		self.assertContains(response,'{"status": "success", "message": "password updated successfully"}')

	def test_recover_password_fail(self):
		user1=User.objects.create(username=os.environ['USERNAME'], 
								email=os.environ['EMAIL'],
								password=os.environ['EMAIL_FORGOT'],
								is_active=True)
		user1.set_password(os.environ['PASSWORD'])
		user1.save()
		hash1 = str(uuid.uuid1())
		obj=user1.forgotpassword_set.create(activation_key=hash1,
											link_time=timezone.now())
		client=Client()
		hash1=os.environ['HASH']		
		password={'password':os.environ['PASSWORD'],
					'password1':os.environ['PASSWORD'],'hash':hash1}
		response=client.post(reverse('recover_password'),
									json.dumps(password),
									content_type="application/json")

		self.assertTrue(response.status_code,200)
		self.assertContains(response,'{"status": "Error", "message": "invalid link or token has been expired."}')

	def test_create_blog(self):
		
		client=Client()
		user1=User.objects.create(username=os.environ['USERNAME'],
		 							email=os.environ['EMAIL'],
		 							password=os.environ['PASSWORD'],
		 							is_active=True)
		user1.set_password(os.environ['PASSWORD'])
		user1.save()
		img=File(open('/home/rizwan/a2.jpg','r'))
		img=str(img)
	 	new_group,created = Group.objects.get_or_create(name='client')
		response=client.post(reverse('loginresult'),
	 						{'username':os.environ['USERNAME'],
	 						'password':os.environ['PASSWORD']})
		Organisation.objects.create(user=user1,
									orgname=os.environ['ORG'],
									orglogo='/home/rizwan/a2.jpg')
		
		categories=Categories.objects.create(name='beauty',state=True)
		response=client.post(reverse('create_blog'),
	 							{'title':os.environ['TITLE'],
	 							'description':os.environ['DESCRIPTION'],
	 							'published':os.environ['PUBLISHED'],
	 							'categories':categories.id,
	 							'user':user1.id	 							
	 						})
		self.assertTrue(response.status_code,200)

	def test_create_blog_fail1(self):
		client=Client()
		user1=User.objects.create(username=os.environ['USERNAME'],
		 							email=os.environ['EMAIL'],
		 							password=os.environ['PASSWORD'],
		 							is_active=True)
		user1.set_password(os.environ['PASSWORD'])
		user1.save()
		img=File(open('/home/rizwan/a2.jpg','r'))
		img=str(img)
	 	new_group,created = Group.objects.get_or_create(name='client')
		response=client.post(reverse('loginresult'),
	 						{'username':os.environ['USERNAME'],
	 						'password':os.environ['PASSWORD']})
		categories=Categories.objects.create(name='beauty',state=True)
		request=HttpRequest()
		request.method='POST'
		request.POST={'title':os.environ['TITLE'],
	  							'description':os.environ['DESCRIPTION'],
	  							'published':os.environ['PUBLISHED'],
	  							'categories':categories.id}
		request.user=user1
		self.assertRaises(ObjectDoesNotExist,views.create_blog,request)
	def test_create_blog_fail2(self):
		client=Client()
		categories=Categories.objects.create(name='beauty',state=True)
		response=client.post(reverse('create_blog'),
	 							{'title':os.environ['TITLE'],
	 							'description':os.environ['DESCRIPTION'],
	 							'published':os.environ['PUBLISHED'],
	 							'categories':categories.id,	 							
	 						})
		self.assertTrue(response.status_code,302)
		self.assertRedirects(response,expected_url='/?next=/create_blog/',
							status_code=302,target_status_code=200)

	def test_delete(self):
		client=Client()
		user1=User.objects.create(username=os.environ['USERNAME'],
		 							email=os.environ['EMAIL'],
		 							password=os.environ['PASSWORD'],
		 							is_active=True)
		user1.set_password(os.environ['PASSWORD'])
		user1.save()
		img=File(open('/home/rizwan/a2.jpg','r'))
		img=str(img)
	 	new_group,created = Group.objects.get_or_create(name='client')
		response=client.post(reverse('loginresult'),
	 						{'username':os.environ['USERNAME'],
	 						'password':os.environ['PASSWORD']}) 
		Organisation.objects.create(user=user1,
									orgname=os.environ['ORG'],
									orglogo='/home/rizwan/a2.jpg')
		org=Organisation.objects.get(user=user1)
		categories=Categories.objects.create(name='beauty',state=True)
		blog=Blog.objects.create(title=os.environ['TITLE'],
									description=os.environ['DESCRIPTION'],
									published=os.environ['PUBLISHED'],
									organisation=org,
									categories=categories)
		
		checkboxes=[]
		checkboxes.insert(0,blog.id)
		response=client.post(reverse('delete_blog'),
	 							{'checkboxes[]':checkboxes,
	 								'user':user1.id
	 							} 							
	 						)
		self.assertTrue(response.status_code,200)
		self.assertContains(response,'{"status": "Success"}')
	
	def test_delete_fail1(self):
		client=Client()
		user1=User.objects.create(username=os.environ['USERNAME'],
		 							email=os.environ['EMAIL'],
		 							password=os.environ['PASSWORD'],
		 							is_active=True)
		user1.set_password(os.environ['PASSWORD'])
		user1.save()
		img=File(open('/home/rizwan/a2.jpg','r'))
		img=str(img)
	 	new_group,created = Group.objects.get_or_create(name='client')
		response=client.post(reverse('loginresult'),
	 						{'username':os.environ['USERNAME'],
	 						'password':os.environ['PASSWORD']}) 
		Organisation.objects.create(user=user1,
									orgname=os.environ['ORG'],
									orglogo='/home/rizwan/a2.jpg')
		org=Organisation.objects.get(user=user1)
		
		checkboxes=[]
		checkboxes.insert(0,"on")
		response=client.post(reverse('delete_blog'),
	 							{'checkboxes[]':checkboxes,
	 								'user':user1.id
	 							} 							
	 						)
		self.assertTrue(response.status_code,200)
		self.assertContains(response,'{"status": "Failure"}')
	

	def test_delete_blog_fail2(self):
		client=Client()
		response=client.post(reverse('manage_blog'))
		self.assertTrue(response.status_code,302)
		self.assertRedirects(response,
							expected_url='/?next=/manage_blog/',
							status_code=302,target_status_code=200)

	def test_manage_blog(self):
		client=Client()
		user1=User.objects.create(username=os.environ['USERNAME'],
		 							email=os.environ['EMAIL'],
		 							password=os.environ['PASSWORD'],
		 							is_active=True)
		user1.set_password(os.environ['PASSWORD'])
		user1.save()
		img=File(open('/home/rizwan/a2.jpg','r'))
		img=str(img)
	 	new_group,created = Group.objects.get_or_create(name='client')
		response=client.post(reverse('loginresult'),
	 						{'username':os.environ['USERNAME'],
	 						'password':os.environ['PASSWORD']})
 
		Organisation.objects.create(user=user1,
									orgname=os.environ['ORG'],
									orglogo='/home/rizwan/a2.jpg')
		org=Organisation.objects.get(user=user1)
		categories=Categories.objects.create(name='beauty',state=True)
		blog=Blog.objects.create(title=os.environ['TITLE'],
									description=os.environ['DESCRIPTION'],
									published=os.environ['PUBLISHED'],
									organisation=org,
									categories=categories)
		response=client.get(reverse('manage_blog'),{'user':user1.id})
		self.assertTrue(response.status_code,200)
		self.assertIn(os.environ['TITLE'],response.content.decode())

	def test_manage_blog_fail(self):
		client=Client()
		response=client.post(reverse('manage_blog'))
		self.assertTrue(response.status_code,302)
		self.assertRedirects(response,
							expected_url='/?next=/manage_blog/',
							status_code=302,
							target_status_code=200)
		

	def test_blogform_valid(self):
	 	categories=Categories.objects.create(name='beauty',state=True)
	 	blogform=BlogForm({'title':os.environ['TITLE'], 
	 						'description':os.environ['DESCRIPTION'],
	 						'categories':categories.id,
	 						'published':os.environ['PUBLISHED']
	 					})
	 	self.assertTrue(blogform.is_valid())
	
	def test_blogform_invalid(self):
	 	categories=Categories.objects.create(name='beauty',state=True)
	 	blogform=BlogForm({'title':os.environ['TITLE'], 
	 						'description':os.environ['DESCRIPTION'],
	 						'published':os.environ['PUBLISHED']
	 						})

	 	self.assertFalse(blogform.is_valid())
	
	def test_update_blog(self):
		client=Client()
		user1=User.objects.create(username=os.environ['USERNAME'],
		 							email=os.environ['EMAIL'],
		 							password=os.environ['PASSWORD'],
		 							is_active=True)
		user1.set_password(os.environ['PASSWORD'])
		user1.save()
		img=File(open('/home/rizwan/a2.jpg','r'))
		img=str(img)
	 	new_group,created = Group.objects.get_or_create(name='client')
		response=client.post(reverse('loginresult'),
	 						{'username':os.environ['USERNAME'],
	 						'password':os.environ['PASSWORD']})
 
		Organisation.objects.create(user=user1,
									orgname=os.environ['ORG'],
									orglogo='/home/rizwan/a2.jpg')
		org=Organisation.objects.get(user=user1)
		categories=Categories.objects.create(name='beauty',state=True)
		blog=Blog.objects.create(title=os.environ['TITLE'],
									description=os.environ['DESCRIPTION'],
									published=os.environ['PUBLISHED'],
									organisation=org,
									categories=categories)
		response=client.post(reverse('update_blog',kwargs={'id':blog.id}),
	 							{'title':os.environ['TITLE'],
	 							'description':os.environ['DESCRIPTION'],
	 							'published':os.environ['PUBLISHED'],
	 							'categories':categories.id,
	 							'id':user1.id	 							
	 						})
		self.assertTrue(response.status_code,302)
		self.assertRedirects(response,
							expected_url='/manage_blog',
							status_code=302,
							target_status_code=301)

	def test_update_delete(self):
		client=Client()
		user1=User.objects.create(username=os.environ['USERNAME'],
		 							email=os.environ['EMAIL'],
		 							password=os.environ['PASSWORD'],
		 							is_active=True)
		user1.set_password(os.environ['PASSWORD'])
		user1.save()
		img=File(open('/home/rizwan/a2.jpg','r'))
		img=str(img)
	 	new_group,created = Group.objects.get_or_create(name='client')
		response=client.post(reverse('loginresult'),
	 						{'username':os.environ['USERNAME'],
	 						'password':os.environ['PASSWORD']})
 
		Organisation.objects.create(user=user1,
									orgname=os.environ['ORG'],
									orglogo='/home/rizwan/a2.jpg')
		org=Organisation.objects.get(user=user1)
		categories=Categories.objects.create(name='beauty',state=True)
		blog=Blog.objects.create(title=os.environ['TITLE'],
									description=os.environ['DESCRIPTION'],
									published=os.environ['PUBLISHED'],
									organisation=org,
									categories=categories)
		blogfile=BlogFile.objects.create(blog_id=blog.id,attachments=img)
		response=client.post(reverse('update_delete_blog'),{'value':blogfile.id})
		self.assertContains(response,'{"status": "Success"}')
	
		
	def test_update_blog_fail(self):
		client=Client()
		user1=User.objects.create(username=os.environ['USERNAME'],
		 							email=os.environ['EMAIL'],
		 							password=os.environ['PASSWORD'],
		 							is_active=True)
		user1.set_password(os.environ['PASSWORD'])
		user1.save()
		img=File(open('/home/rizwan/a2.jpg','r'))
		img=str(img)
	 	new_group,created = Group.objects.get_or_create(name='client')
		response=client.post(reverse('loginresult'),
	 						{'username':os.environ['USERNAME'],
	 						'password':os.environ['PASSWORD']})
 
		Organisation.objects.create(user=user1,
									orgname=os.environ['ORG'],
									orglogo='/home/rizwan/a2.jpg')
		org=Organisation.objects.get(user=user1)
		request=HttpRequest()
		request.method='GET'
		request.user=user1
		self.assertRaises(ObjectDoesNotExist,views.update_blog,request,id=2)

	def test_detail_blog(self):
		client=Client()
		user1=User.objects.create(username=os.environ['USERNAME'],
		 							email=os.environ['EMAIL'],
		 							password=os.environ['PASSWORD'],
		 							is_active=True)
		user1.set_password(os.environ['PASSWORD'])
		user1.save()
		img=File(open('/home/rizwan/a2.jpg','r'))
		img=str(img)
	 	new_group,created = Group.objects.get_or_create(name='client')
		response=client.post(reverse('loginresult'),
	 						{'username':os.environ['USERNAME'],
	 						'password':os.environ['PASSWORD']})
 
		Organisation.objects.create(user=user1,
									orgname=os.environ['ORG'],
									orglogo='/home/rizwan/a2.jpg')
		org=Organisation.objects.get(user=user1)
		categories=Categories.objects.create(name='beauty',state=True)
		blog=Blog.objects.create(title=os.environ['TITLE'],
									description=os.environ['DESCRIPTION'],
									published=os.environ['PUBLISHED'],
									organisation=org,
									categories=categories)
		blogfile=BlogFile.objects.create(blog_id=blog.id,attachments=img)
		response=client.get(reverse('detail_blog',kwargs={'id':blog.id}))
		self.assertTrue(response.status_code,200)

	def test_detail_blog_fail(self):
		client=Client()
		user1=User.objects.create(username=os.environ['USERNAME'],
		 							email=os.environ['EMAIL'],
		 							password=os.environ['PASSWORD'],
		 							is_active=True)
		user1.set_password(os.environ['PASSWORD'])
		user1.save()
		img=File(open('/home/rizwan/a2.jpg','r'))
		img=str(img)
	 	new_group,created = Group.objects.get_or_create(name='client')
		response=client.post(reverse('loginresult'),
	 						{'username':os.environ['USERNAME'],
	 						'password':os.environ['PASSWORD']})
		response=client.get(reverse('detail_blog',kwargs={'id':23}))
		self.assertFalse(response.status_code,404)		
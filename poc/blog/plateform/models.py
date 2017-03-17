from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Status(models.Model):
	pr_status=models.CharField(max_length=15) 

class Role(models.Model):
	pr_role=models.CharField(max_length=10)

class RegisteredUser(models.Model):
	user=models.OneToOneField(User, on_delete=models.CASCADE)
	status=models.ForeignKey(Status,default='1',on_delete=models.CASCADE)
	role=models.ForeignKey(Role,default='3',on_delete=models.CASCADE)

class Organisation(models.Model):
	orguser=models.OneToOneField(User, on_delete=models.CASCADE)
	orgname=models.CharField(max_length=225)
	description=models.CharField(max_length=225)
	orglogo=models.ImageField(upload_to='Companylogo')
	status=models.ForeignKey(Status,default='2',on_delete=models.CASCADE)
	role=models.ForeignKey(Role,default='2',on_delete=models.CASCADE)

class Organisation_address(models.Model):
	organisation=models.ForeignKey(Organisation,on_delete=models.CASCADE)
	address=models.CharField(max_length=500)
	contactno=models.CharField(max_length=16, blank=True)

class Organisation_socialaccount(models.Model):
	organisation=models.ForeignKey(Organisation,on_delete=models.CASCADE)
	faceaccount=models.CharField(max_length=125)
	twitaccount=models.CharField(max_length=125)

class Blog(models.Model):
	blogtitle=models.CharField(max_length=225)
	blogdescription=models.CharField(max_length=225)
	blogimage=models.ImageField(upload_to='Companyblog')
	posted=models.BooleanField(default=False)


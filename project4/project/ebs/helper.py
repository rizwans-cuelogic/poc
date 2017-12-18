import json
import os
import uuid
import sys
from datetime import datetime, timedelta
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string, get_template
from django.utils import timezone
from django.utils.html import strip_tags
from django.db.models import Count
from .models import Organisation,Blog,BlogFile,ForgotPassword,Categories



def get_banner_blogs(main_blog):

	
	banner_context={}
	banner_data=list()
	blogs=Blog.objects.filter(published_state=True).order_by('-id')
	blogs=blogs.exclude(id=main_blog.id)

	for each in blogs:
		banner_context={'banner_id':each.id,
				'banner_title':each.title,
				'banner_categories':each.categories,
				'banner_timestamp':each.published,
				'banner_organisation':each.organisation
		}
		files=BlogFile.objects.filter(blog_id=each.id)
		if not files :
			continue
		else:
			for file in files:
				banner_context['banner_file']=file.attachments
				blogs=blogs.exclude(id=each.id)
				banner_data.append(banner_context)
		if len(banner_data)==4:
			break

	return banner_data,blogs


def get_latest_blogs(blogs):
	latest_context={}
	latest_data=list()
	for each in blogs:
		latest_context={'latest_id':each.id,
					'latest_title':each.title,
					'latest_categories':each.categories,
					'latest_timestamp':each.published,
					'latest_organisation':each.organisation
				}
		files=BlogFile.objects.filter(blog_id=each.id)
		if not files :
			continue
		else:
			for file in files:
				latest_context['latest_file']=file.attachments
			blogs=blogs.exclude(id=each.id)
		latest_data.append(latest_context)
		if len(latest_data)==10:
			break
	return latest_data,blogs


def get_popular_blogs(blogs):

	popular_context={}    
	#popular_data=get_popular_blogs(blogs)
	popular_data=list()
	for each in blogs:
		popular_context={'popular_id':each.id,
		'popular_title':each.title,
		'popular_categories':each.categories,
		'popular_timestamp':each.published,
		'popular_organisation':each.organisation
		}
		files=BlogFile.objects.filter(blog_id=each.id)
		if not files :
			continue
		else:
			for file in files:
				popular_context['popular_file']=file.attachments
			blogs=blogs.exclude(id=each.id)
		popular_data.append(popular_context)
		if len(popular_data)==4:
			break

	return popular_data,blogs

def send_email(user,hash1,subject):

	subject = subject
	html_content = render_to_string(
		'ebs/mail.html', 
		{'hash1': hash1, 
		'HOST': settings.HOST,
		'user': user})

	text_content = strip_tags(html_content)
	from_email = settings.EMAIL_HOST_USER
	msg = EmailMultiAlternatives(
		subject, text_content, from_email, [user.email])
	msg.attach_alternative(html_content, "text/html")
	msg.send()


def filter_manage_blog(query,filters,bloglist):

	if query or filters:
		if filters=='en':
			bloglist=bloglist.filter(published_state=True)
		elif filters=='ds':
			bloglist=bloglist.filter(published_state=False)    
		bloglist=bloglist.filter(
			Q(title__icontains=query)|
			Q(description__icontains=query)|
			Q(tags__icontains=query)
			)	

	return bloglist

def get_related_blogs(related_blog):
	related_data = list()
	related_context = {}
	for each in related_blog:
		related_context={
		'related_id':each.id,
		'related_title':each.title,
		'related_timestamp':each.published,
		'related_categories':each.categories
		}
		files=BlogFile.objects.filter(blog_id=each.id)
		if not files :
			continue
		else:
			for each in files:
				related_context['related_file']=each.attachments
				break
		related_data.append(related_context)

	return related_data

def check_password_empty(password):
	if password == '':
		response = {'status': 'Error',
					'message': "please fill the details"}
		return HttpResponse(json.dumps(response),
							content_type='application/json')
	return

def check_password_length(password):

	if len(password) < 8 or len(password) > 16:
		response = {'status': 'Error',
					'message': "please fill the details"}
		return HttpResponse(json.dumps(response),
							content_type='application/json')
	return

def check_password_match(REGEX,password):

	if REGEX.match(password) is None:
		response = {'status': 'Error',
					'message': "please fill the details"}
		return HttpResponse(json.dumps(response), 
							content_type='application/json')
	return

def check_confirm_password_match(password,password1):
	
	if password!=password1:
		response = {'status': 'Error',
					'message': "please fill the details"}
		return HttpResponse(json.dumps(response), 
							content_type='application/json')
	return

def find_related_blog_tags(bloginstance):

	if bloginstance.tags: 
		related_blog=Blog.objects.filter(
							Q(published_state=True) &
							(Q(categories=bloginstance.categories)|
							Q(tags__icontains=bloginstance.tags))).order_by('-id')
	else:
		related_blog=Blog.objects.filter(
								Q(published_state=True)&
								Q(categories=bloginstance.categories)).order_by('-id')

	return related_blog

def get_expiry_time():
	return (timezone.now() - timedelta(hours=48))
import json
import hashlib
import os
import uuid
import sys
import re
import imghdr
from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import (authenticate, login, logout,)
from django.contrib.auth.decorators import login_required
from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.http import Http404
from django.template.loader import render_to_string, get_template
from django.utils import timezone
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from .models import Organisation,Blog,BlogFile,ForgotPassword
from .forms import UserForm, OrgForm, UserLoginForm,BlogForm,BlogFileForm
# Create your views here.


def home(request):
    userform = UserForm()
    orgform = OrgForm()
    loginform = UserLoginForm()
    hash1 = request.GET.get('uid', '')
    try:
        if (hash1):
            obj = ForgotPassword.objects.get(activation_key=hash1)
            user = User.objects.get(username=obj.username)
            time_date = obj.link_time
            if time_date < (timezone.now() - timedelta(hours=48)):
                return render(request, 'ebs/home.html', {'userform': userform,
                                                        'orgform': orgform, 
                                                        'loginform': loginform,
                                                        'hashsuccess': False})
            else:
                return render(request, 'ebs/home.html', {'userform': userform, 
                                                        'orgform': orgform, 
                                                        'loginform': loginform,
                                                        'hashsuccess': True,
                                                        'hash': hash1})
    except Exception:
        return render(request, 'ebs/home.html', {'userform': userform,
                                                'orgform': orgform,
                                                'loginform': loginform, 
                                                'hashsuccess': False})

    return render(request, 'ebs/home.html', {'userform': userform,
                                            'orgform': orgform,
                                            'loginform': loginform})


def newpassword(request):
    return render(request, 'ebs/newpassword.html')


def register(request):
    """Views for registering client to plateform take UserForm and OrgForm save it to User object
    and organisation object"""
    if request.method == 'POST':
        userform = UserForm(request.POST or None, request.FILES or None)
        orgform = OrgForm(request.POST or None, request.FILES or None)
        if userform.is_valid() and orgform.is_valid():
            user = User.objects.create_user(userform.cleaned_data['username'],
                                            userform.cleaned_data['email'],
                                            userform.cleaned_data['password'],
                                            is_active='False')
            organisation = orgform.save(commit=False)
            organisation.user = user
            g = Group.objects.get(name='client')
            g.user_set.add(user)
            organisation.save()
            user.save()
            response = {'status': 'success', 'message': 'Your account has been created and pending for admin approval.  You will get an email after admin approval on your registered email id. This process will take 24 hours.'}
            return HttpResponse(json.dumps(response), 
                        content_type='application/json')

        else:
            error = json.dumps(userform.errors)
            errorstring = json.loads(error)
            if 'username' in errorstring and errorstring['username'] == [u'username already exists']:
                response = {'status': 'Error',
                            'message': "username already exists"}
            elif 'email' in errorstring and errorstring['email'] == [u'Email already exists']:
                response = {'status': 'Error',
                            'message': "email already exists"}
            else:
                response = {'status': 'Error',
                            'message': "please fill the details"}

            return HttpResponse(json.dumps(response), 
                                content_type='application/json')
    else:
        userform = UserForm()
        orgform = OrgForm()
        loginform = UserLoginForm()
        return render(request, 'ebs/home.html', 
                                {'userform': userform, 
                                'orgform': orgform, 
                                'loginform': loginform})


def loginresult(request):
    userform = UserForm()
    orgform = OrgForm()
    loginform = UserLoginForm()
    if request.method == 'POST':
        loginform = UserLoginForm(request.POST or None)
        if loginform.is_valid():
            username = loginform.cleaned_data['username']
            password = loginform.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    response = {'status': 'success',
                                'message': "good"}
                    return HttpResponse(json.dumps(response), 
                                        content_type='application/json')
                else:
                    response = {'status': 'Error',
                                'message': "User is inactive try again"}
            else:
                response = {'status': 'Error',
                            'message': "Invalid Username And Password"}
            return HttpResponse(json.dumps(response), 
                                content_type='application/json')


def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')


def forgotpass(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            email = data['email']
            user = User.objects.get(email=email)
            if user.is_active:
                hash1 = str(uuid.uuid1())
                obj = user.forgotpassword_set.create(
                    activation_key=hash1, link_time=timezone.now())
                subject = 'Password Recovery'
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
                response = {
                'status': 'success', 'message': "Reset password link has been email to your registered email address."}
                return HttpResponse(json.dumps(response), 
                                    content_type='application/json')
            else:
                response = {'status': 'Error', 'message': "Invalid email"}
                return HttpResponse(json.dumps(response), 
                                    content_type='application/json')

    except Exception as e:
        print e
        response = {'status': 'Error', 'message': "Invalid email"}
        return HttpResponse(json.dumps(response), content_type='application/json')


def recover_password(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            hash1 = data['hash']
            password = data['password']
            password1=data['password1']
            REGEX = re.compile('^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[a-zA-z\d]+$')
            if password == '':
                response = {'status': 'Error',
                            'message': "please fill the details"}
                return HttpResponse(json.dumps(response),
                                     content_type='application/json')
            elif len(password) < 8 or len(password) > 16:
                response = {'status': 'Error',
                            'message': "please fill the details"}
                return HttpResponse(json.dumps(response),
                                    content_type='application/json')

            elif REGEX.match(password) is None:
                response = {'status': 'Error',
                            'message': "please fill the details"}
                return HttpResponse(json.dumps(response), 
                                    content_type='application/json')

            elif password!=password1:
                response = {'status': 'Error',
                            'message': "please fill the details"}
                return HttpResponse(json.dumps(response), 
                                    content_type='application/json')
            obj = ForgotPassword.objects.get(activation_key=hash1)
            user = User.objects.get(username=obj.username)
            user.set_password(password)
            user.save()
            ForgotPassword.objects.get(id=obj.id).delete()
            response = {'status': 'success',
                        'message': "password updated successfully"}
            return HttpResponse(json.dumps(response), 
                                content_type='application/json')

    except Exception as e:
        response = {'status': 'Error', 'message': 'invalid link or token has been expired.'}
        return HttpResponse(json.dumps(response), 
                            content_type='application/json')

@login_required(login_url='/')
def create_blog(request):
    if request.method=='POST':
        blogform=BlogForm(request.POST or None,request.FILES or None)
        blogfileform=BlogFileForm(request.POST or None,request.FILES or None)
        if blogform.is_valid() and  blogfileform.is_valid():
            files = request.FILES.values()
            blog=blogform.save(commit=False)
            orgobj=Organisation.objects.get(user_id=request.user.id)
            blog.organisation_id=orgobj.id
            if 'button1' in request.POST:
                blog.draft=True
            blog.save()
            for a_file in files:
                instance=BlogFile()
                instance.blog_id=blog.id
                instance.attachments=a_file
                instance.save()
            blog.save()
            messages.success(request, 'Blog details saved successfully.')
            return HttpResponseRedirect('/manage_blog',{"messages":messages})
    else:
        blogfileform=BlogFileForm()
        blogform=BlogForm()
        return render(request,'ebs/create_blog.html',{'blogform': blogform,'blogfileform':blogfileform})

@login_required(login_url='/')
def manage_blog(request):
    try:
        orgobj=Organisation.objects.get(user_id=request.user.id)   
        data=list()
        context={}
        bloglist=Blog.objects.filter(organisation_id=orgobj.id).order_by('-timestamp')
        for each in bloglist:
            context={'blog_id':each.id,
                'blog_title':each.title,
                'blog_description':each.description
            }
            files=BlogFile.objects.filter(blog_id=each.id)
            if files is None:
                context['blog_file']=''
            else:
                count=0
                for each in files:
                    filename, file_extension = os.path.splitext(str(each.attachments))
                    if  file_extension in ['.png','.jpeg','.jpg'] and count==0:
                        count+=1
                        context['blog_file']=each.attachments

            data.append(context)
        return render(request, 'ebs/manage_blog.html',{'data':data})
    except :
        return render(request,'ebs/manage_blog.html')

@csrf_exempt
def delete_blog(request):
    import pdb
    pdb.set_trace()
    newdata = request.user
    orgdata = Organisation.objects.get(user_id=newdata.id)
    swid = request.POST.getlist('checkbox[]') 
    for one in swid:
        obj = Blog.objects.get(id=one).delete()

    response = json.dumps({'data':'deleted'})
    return HttpResponse(response, mimetype="application/json")
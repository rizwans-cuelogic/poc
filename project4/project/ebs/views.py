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
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Q
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
        query=request.GET.get('q')
        filters=request.GET.get('filterbox') 
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

        for each in bloglist:
            context={'blog_id':each.id,
                'blog_title':each.title,
                'blog_description':each.description
            }
            files=BlogFile.objects.filter(blog_id=each.id).order_by('-id')
            if files is None:
                context['blog_file']=''
            else:
                for each in files:
                    print each.attachments
                    filename, file_extension = os.path.splitext(str(each.attachments))
                    if  file_extension in ['.png','.jpeg','.jpg']:
                        context['blog_file']=each.attachments
                        break

            data.append(context)
        paginator=Paginator(data,5)
        page = request.GET.get('page')
        try:
            datas=paginator.page(page)
        except PageNotAnInteger:
            datas=paginator.page(1)
        except EmptyPage:
            datas=paginator.page(paginator.num_pages)
        return render(request, 'ebs/manage_blog.html',
                        {'datas':datas,'page':page})
    except :
        return render(request,'ebs/manage_blog.html')

@csrf_exempt
def delete_blog(request):
    try:
        orgdata = Organisation.objects.get(user_id=request.user.id)
        swid = request.POST.getlist('checkboxes[]')
        if swid[0]=='on':
            swid.pop(0)
        if len(swid)==0:
            response = json.dumps({'status':'Failure'})
            return HttpResponse(response, content_type="application/json")
        for one in swid:
            obj = Blog.objects.get(id=one).delete()
            BlogFile.objects.filter(blog_id=one).delete()

        response = json.dumps({'status':'Success'})
        return HttpResponse(response, content_type="application/json")
    except:
        response = json.dumps({'status':'Failure'})
        return HttpResponse(response, content_type="application/json")

def update_blog(request,id):
    bloginstance=Blog.objects.get(id=id)
    fileinstance=BlogFile.objects.filter(blog=id)
    if request.method=='POST':
        blogform=BlogForm(request.POST or None,request.FILES or None,instance=bloginstance)
        blogfileform=BlogFileForm(request.POST or None,request.FILES or None)
        if blogform.is_valid() and  blogfileform.is_valid():
            files = request.FILES.values()
            blog=blogform.save(commit=False)
            orgobj=Organisation.objects.get(user_id=request.user.id)
            blog.organisation_id=orgobj.id
            if 'button1' in request.POST:
                blog.draft=True
                blog.published_state=False
            else:
                blog.draft=False
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
        
        blogform=BlogForm(instance=bloginstance)
        attachments_value= ""
        image1_value=""
        image2_value=""
        attachments_id=0
        image1_id=0
        image2_id=0
        if not fileinstance:
            pass
        if len(fileinstance)==1:
            attachments_value=fileinstance[0].attachments.name
            attachments_id=fileinstance[0].id
        if len(fileinstance)==2:
            attachments_value=fileinstance[0].attachments.name
            image1_value=fileinstance[1].attachments.name
            attachments_id=fileinstance[0].id
            image1_id=fileinstance[1].id          
        if len(fileinstance)==3:
            attachments_value=fileinstance[0].attachments.name
            image1_value=fileinstance[1].attachments.name
            image2_value=fileinstance[2].attachments.name
            attachments_id=fileinstance[0].id
            image1_id=fileinstance[1].id
            image2_id=fileinstance[2].id      
        blogfileform=BlogFileForm(request.POST)                      
        return render(request,'ebs/update_blog.html',
                                    {'blogform':blogform,'blogfileform':blogfileform,
                                    'bloginstance':bloginstance,
                                    'attachments_value':attachments_value,
                                    'image1_value':image1_value,
                                    'image2_value':image2_value,
                                    'attachments_id':attachments_id,
                                    'image1_id':image1_id,
                                    'image2_id':image2_id})
@csrf_exempt
def update_delete_blog(request):
    if request.method=='POST':
        value=request.POST.get('value')
        file=BlogFile.objects.get(id=value)
        file.delete()
        response = json.dumps({'status':'Success'})
        return HttpResponse(response, content_type="application/json")

def detail_blog(request,id):
    bloginstance=Blog.objects.get(id=id)
    fileinstance=BlogFile.objects.filter(blog=id)
    related_blog=Blog.objects.filter(categories=bloginstance.categories)
    related_blog=related_blog.exclude(id=id)
    related_context={}
    related_data=list()
    pdf_data=list()
    image_data=list()
    for each in fileinstance:
        filename, file_extension = os.path.splitext(str(each.attachments))
        if  file_extension in ['.png','.jpeg','.jpg']:
            image_data.append(each)
        else:
            pdf_data.append(each)
    print "pdf",pdf_data
    print "image",image_data
    for each in related_blog:
        related_context={
                'related_id':each.id,
                'related_title':each.title,
                'related_timestamp':each.timestamp,
                'related_categories':each.categories
            }
        files=BlogFile.objects.filter(blog_id=each.id).order_by('-id')
        if files is None:
            related_context['related_file']=''
        else:
            for each in files:
                print each.attachments
                filename, file_extension = os.path.splitext(str(each.attachments))
                if  file_extension in ['.png','.jpeg','.jpg']:
                    related_context['related_file']=each.attachments
                    break
        related_data.append(related_context)

    print related_blog
    print related_data
    return render(request, 'ebs/detail_blog.html',
                        {'blog':bloginstance,'image_data':image_data,'pdf_data':pdf_data},related_context)


from __future__ import unicode_literals
from datetime import datetime, timedelta
from django.contrib.auth.models import User 
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.db.models import signals
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives


class Organisation(models.Model):
    """Organisation(client) model for storing client information"""
    user = models.OneToOneField(User)
    orgname = models.CharField(max_length=125)
    description = models.TextField(blank=True, null=True)
    orglogo = models.ImageField(upload_to='Companylogo/')

    def __unicode__(self):
        return 'Organisation :' + self.orgname


def send_notification(sender, instance, *args, **kwargs):
    """function take single user object check whether field is_active is changed 
            to true and if it is
            true send email to user"""
    try:
        if instance.is_active != User.objects.get(id=instance.id).is_active and instance.is_active == True:
            print "created is"
            subject = 'Welcome To News Magzine'
            html_content = render_to_string(
                'ebs/welcomemail.html', {'HOST': settings.HOST})
            text_content = strip_tags(html_content)
            from_email = settings.EMAIL_HOST_USER
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [instance.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        else:
            pass
    except:
        print "can not send email"

pre_save.connect(send_notification, sender=User)


class forgotpassword(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=50)
    link_time = models.DateTimeField(default=datetime.now, blank=True)

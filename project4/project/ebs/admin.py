from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags
from ebs.models import Organisation


admin.site.register(Organisation)


class OrganisationInline(admin.StackedInline):
    model = Organisation
    can_delete = False


def mark_inactive(ModelAdmin, request, queryset):
    """for  adding deactivate action in admin """
    queryset.update(is_active=False)


def mark_active(ModelAdmin, request, queryset):
    """for adding activate action in admin as well as sending email to all users"""
    queryset.update(is_active=True)
    for obj in queryset:
        subject = 'Welcome to NewsMagzine'
        html_content = render_to_string(
            'ebs/welcomemail.html', {'HOST': settings.HOST})
        text_content = strip_tags(html_content)
        from_email = settings.EMAIL_HOST_USER
        msg = EmailMultiAlternatives(
            subject, text_content, from_email, [obj.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
mark_inactive.short_description = "Deactivate selected users"
mark_active.short_description = "Activate selected users"


class UserAdmin(UserAdmin):
    """for customizing user object table as well as adding actions in admin"""
    inlines = (OrganisationInline,)
    list_display = ('username', 'email', 'is_active',
                    'date_joined', 'display_orgname')
    ordering = ['username']
    actions = [mark_inactive, mark_active]

    def display_orgname(self, request):
        if Organisation.objects.filter(user__id=request.id):
            return 'Client'
    display_orgname.short_description = 'Role'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

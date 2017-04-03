from django.contrib import admin
from ebs.models import Organisation
from django.contrib.auth.admin import UserAdmin
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User


admin.site.register(Organisation)

class OrganisationInline(admin.StackedInline):
    model = Organisation
    can_delete = False

def mark_inactive(ModelAdmin,request,queryset):
	"""for  adding deactivate action in admin """
	queryset.update(is_active=False)

def mark_active(ModelAdmin,request,queryset):
	"""for adding activate action in admin as well as sending email to all users"""
	queryset.update(is_active=True)
	for obj in queryset:
		subject = 'Active account'
 		mesagge = '%s Your account has been activated now. You can login and add blogs. Click here to login.' %(obj.username)
 		from_email = settings.EMAIL_HOST_USER
 		send_mail(subject, mesagge, from_email, [obj.email], fail_silently=True)
	

	
mark_inactive.short_description = "Deactivate selected users"
mark_active.short_description = "Activate selected users"

class UserAdmin(UserAdmin):
	"""for customizing user object table as well as adding actions in admin"""
	inlines=(OrganisationInline,)
	list_display = ('username', 'email','is_active', 'date_joined','display_orgname')
	ordering=['username']	
	actions=[mark_inactive,mark_active]
	def display_orgname(self, request):
		if Organisation.objects.filter(user__id = request.id):
			return 'Client'
	display_orgname.short_description = 'Role'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from ebs.models import Organisation,Blog,Catagories
from functools import partial
from bootstrap3_datetime.widgets import DateTimePicker

class UserForm(forms.ModelForm):
	password=forms.CharField(label="Password" , 
					widget=forms.PasswordInput(
							attrs={'size':'100%' , 
								   'class':'form-control',
								   'data-minlength':'8',
								   'data-maxlength':'16'}))
	password1=forms.CharField(label="Passwordconfirm", 
					widget=forms.PasswordInput(
							attrs={'size':'100%' , 
									'class':'form-control',
									'data-minlength':'8',
									'data-maxlength':'16'}))
	username=forms.CharField(label="Username" , 
					widget=forms.TextInput(
							attrs={'size':'100%' , 
									'class':'form-control',
									'data-minlength':'6'}))
	email=forms.EmailField(label="Email", 
					widget=forms.TextInput(
							attrs={'size':'100%' , 
									'class':'form-control'}))
	class Meta:
		model=User
		fields=['username','email','password']
		exclude=['first_name','last_name',]
	def clean_username(self):
		if User.objects.filter(username=self.cleaned_data['username']).exists():
			raise forms.ValidationError("username already exists")
		return self.cleaned_data['username']

	def clean_email(self):
		if User.objects.filter(email=self.cleaned_data['email']).exists():
			raise forms.ValidationError("Email already exists")
		return self.cleaned_data['email']

class OrgForm(forms.ModelForm):
	orgname=forms.CharField(label="Orgname",
					widget=forms.TextInput(
							attrs={'size':'100%', 
									'class':'form-control'}))
	orglogo=forms.ImageField(label="Orglogo",
					widget=forms.FileInput(
							attrs={'size':'100%', 
									'class':'form-control'}))
	class Meta:
		model= Organisation
		fields=['orgname','orglogo',]
		exclude=['user','description',]


class UserLoginForm(forms.Form):
	username=forms.CharField(label="Username" ,
					widget=forms.TextInput(
							attrs={'size':'100%' , 
									'class':'form-control',
									'data-minlength':'6'}))

	password=forms.CharField(label="Password" , 
					widget=forms.PasswordInput(
							attrs={'size':'100%' , 
								   'class':'form-control',
								   'data-minlength':'8',
								   'data-maxlength':'16'}))

DateInput=partial(forms.DateInput, {'class' : 'datepicker' })
class BlogForm(forms.ModelForm):
	title=forms.CharField(required=True,label="title",
					widget=forms.TextInput(
						attrs={'size':'100%',
								'placeholder':'Title',
							   'class':'form-control',
							   }))
	description = forms.CharField(required=True,label="description",
							widget=forms.Textarea(
								attrs={'size': '100%',
									   'class': 'form-control'}))
	tags= forms.CharField(required='false',label="title",
						widget=forms.TextInput(
							 attrs={'size': '100%',
									'class': 'form-control'}))
	
	published=forms.DateTimeField(
          				required=True,
          				widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm",
          												"pickSeconds":False}))

	catagories=forms.ModelChoiceField(queryset=Catagories.objects.all().filter(state=True).order_by('name'),
									  empty_label='Select Catagory',widget=forms.Select(attrs={
          'class':'catagory' 
          }))
	commentstate=forms.BooleanField(required=False)

	class Meta:
			model=Blog
			fields=[
				"title",
				"description",
				"tags",
				"published",
				"catagories",
				"commentstate"
			]

class BlogFileForm(forms.Form):
	attachments=forms.FileField(required=False,label="image",
						widget=forms.FileInput(
							attrs={'size':'50%',
								   'class':'form-control file-width'}))
	image1=forms.FileField(required=False,label="image",
						widget=forms.FileInput(
							attrs={'size':'50%',
								   'class':'form-control file-width'}))
	image2=forms.FileField(required=False,label="image",
						widget=forms.FileInput(
							attrs={'size':'50%',
								   'class':'form-control file-width'}))
	

from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from ebs.models import Organisation,Blog ,Categories
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
	TRUE_FALSE_CHOICE = (
    (True, "Enable"),
    (False, "Disable")
	)
	title=forms.CharField(max_length=125,required=True,label="title",
					widget=forms.TextInput(
						attrs={
								'placeholder':'Title',
							   'class':'form-control',

							   }))
	description = forms.CharField(required=True,label="description",
							widget=forms.Textarea(
								attrs={
									   'placeholder':'Add Description',
									   'class': 'form-control',
									    'rows': '10',
                						'cols': '90',
                						'maxlength': '2000',}))
	tags= forms.CharField(max_length=100,required=False,label="title",
						widget=forms.TextInput(
							 attrs={
							 		'placeholder':'Tags',
									'class': 'form-control'}))
	
	published=forms.DateTimeField(
          				required=True,
          				widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm "}))

	categories=forms.ModelChoiceField(
						queryset=Categories.objects.all().filter(state=True).order_by('name'),
						empty_label='Select Catagory',
						widget=forms.Select(attrs={"class":"catagory form-control" })
					)
	comment_state=forms.BooleanField(required=False)

	published_state = forms.ChoiceField(choices = TRUE_FALSE_CHOICE, label="Somelabel", 
                         		widget=forms.Select(attrs={"class":"catagory form-control" }), required=False,
                         )
	class Meta:
			model=Blog
			fields=[
				"title",
				"description",
				"tags",
				"published",
				"categories",
				"comment_state",
				"published_state"
			]

class BlogFileForm(forms.Form):
	attachments=forms.FileField(required=False,label="image",
						widget=forms.FileInput(
							attrs={
								   'class':'form-control blog-file',
								   'accept':'image/jpeg,image/png,application/msword,application/vnd.ms-excel,application/pdf'
								}))
	image1=forms.FileField(required=False,label="image",
						widget=forms.FileInput(
							attrs={
								   'class':'form-control blog-file',
								   'accept':'image/jpeg,image/png,application/msword,application/vnd.ms-excel,application/pdf'
								}))
	image2=forms.FileField(required=False,label="image",
						widget=forms.FileInput(
							attrs={
								   'class':'form-control blog-file',
								   'accept':'image/jpeg,image/png,application/msword,application/vnd.ms-excel,application/pdf'
								}))
	
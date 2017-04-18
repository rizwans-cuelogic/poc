from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
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

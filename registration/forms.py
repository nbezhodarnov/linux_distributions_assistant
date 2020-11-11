from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import TextInput, PasswordInput
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('username', 'password1', 'password2')
		
		widgets = {
			"username": TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Имя пользователя'
			})
		}
	
	def __init__(self, *args, **kwargs):
		super(UserRegistrationForm, self).__init__(*args, **kwargs)
		self.fields['password1'].widget = PasswordInput(attrs={
			'class': 'form-control',
			'placeholder': 'Пароль'
		})
		self.fields['password2'].widget = PasswordInput(attrs={
			'class': 'form-control',
			'placeholder': 'Подтверждение пароля'
		})

class UserLoginForm(AuthenticationForm):
	class Meta:
		model = User
		fields = ('username', 'password')
		
		widgets = {
			"username": TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Имя пользователя'
			})
		}
	
	def __init__(self, *args, **kwargs):
		super(UserLoginForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget = TextInput(attrs={
			'class': 'form-control',
			'placeholder': 'Имя пользователя'
		})
		self.fields['password'].widget = PasswordInput(attrs={
			'class': 'form-control',
			'placeholder': 'Пароль'
		})

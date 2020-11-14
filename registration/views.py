from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView
from . import forms

# Create your views here.

class UserRegistrationFormView(FormView):
	form_class = forms.UserRegistrationForm
	success_url = "/accounts/login"
	template_name = "registration/register.html"
	
	def get(self, request, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect('/', {'user': self.request.user})
		return super(UserRegistrationFormView, self).get(request, *args, **kwargs)
	
	def form_valid(self, form):
		form.save()
		return super(UserRegistrationFormView, self).form_valid(form)
	
	def form_invalid(self, form):
		return super(UserRegistrationFormView, self).form_invalid(form)

class UserLoginFormView(LoginView):
	form_class = forms.UserLoginForm
	success_url = "/"
	template_name = 'registration/login.html'
	
	def get(self, request, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect('/', {'user': self.request.user})
		return super(UserLoginFormView, self).get(request, *args, **kwargs)
	
	def form_valid(self, form):
		return super(UserLoginFormView, self).form_valid(form)

def index(request):
	return render(request, 'registration/login.html')

def userlogout(request):
	logout(request)
	return redirect(request.META.get('HTTP_REFERER'))

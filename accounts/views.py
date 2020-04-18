from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render

from .forms import SignupForm


class Login(LoginView):
	success_url = reverse_lazy('home')
	template_name = 'registration/login.html'


class SignUp(SuccessMessageMixin, generic.CreateView):
	form_class = SignupForm
	success_url = reverse_lazy('accounts:login')
	success_message = "حساب کاربری شما با موفقیت ساخته شد. می‌توانید وارد شوید!"
	template_name = 'registration/signup.html'

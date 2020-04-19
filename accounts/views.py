from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, redirect_to_login
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import SignupForm, PasswordResetConfirmForm


class Login(LoginView):
	redirect_authenticated_user = True
	success_url = reverse_lazy('home')
	template_name = 'registration/login.html'

class SignUp(UserPassesTestMixin, SuccessMessageMixin, generic.CreateView):

	def test_func(self):
		return self.request.user.is_anonymous

	login_url = reverse_lazy('home')

	def handle_no_permission(self):
		return redirect('home')
	form_class = SignupForm
	success_url = reverse_lazy('accounts:login')
	success_message = "حساب کاربری شما با موفقیت ساخته شد. می‌توانید وارد شوید!"
	template_name = 'registration/signup.html'


class PasswordReset(PasswordResetView):
	success_url = reverse_lazy('accounts:password_reset_done')


class PasswordResetConfirm(SuccessMessageMixin, PasswordResetConfirmView):
	form_class = PasswordResetConfirmForm
	success_message = "گذرواژه‌ی شما با موفقیت تغییر کرد. می‌توانید با گذرواژه‌ی جدید به حساب‌تان وارد شوید."
	success_url = reverse_lazy('accounts:login')

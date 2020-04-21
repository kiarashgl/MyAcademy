from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, redirect_to_login
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import SignupForm, PasswordResetConfirmForm, EditProfileForm
from .models import User


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


class Profile(generic.detail.DetailView):
	model = User
	template_name = 'registration/profile.html'

	def get_object(self, queryset=None):
		return self.request.user

	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect('accounts:login')

		return super(Profile, self).get(request, *args, **kwargs)


class EditProfile(generic.edit.UpdateView):
	form_class = EditProfileForm
	success_url = reverse_lazy('accounts:profile')
	success_message = "پروفایل شما با موفقیت به روزرسانی شد."
	template_name = 'registration/profile_edit.html'

	def get_object(self, queryset=None):
		return self.request.user

	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect('accounts:login')

		return super(EditProfile, self).post(request, *args, **kwargs)

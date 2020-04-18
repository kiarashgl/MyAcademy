from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User

class SignupForm(UserCreationForm):
	# Suppress help texts
	def __init__(self, *args, **kwargs):
		super(UserCreationForm, self).__init__(*args, **kwargs)
		for fieldname in ['username', 'password1', 'password2']:
			self.fields[fieldname].help_text = None
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_class = 'form-horizontal col-md-10 mx-auto'
		self.helper.label_class = 'col-lg-12'
		self.helper.field_class = 'col'
		self.helper.use_custom_control = True
		self.helper.layout = Layout(
			Div('username', css_class='ltr-form'),
			Div(
				Div('first_name', css_class='col'),
				Div('last_name', css_class='col'),
				css_class='row'
			),
			Div('email', css_class='ltr-form'),
			Div('password1', css_class='ltr-form'),
			Div('password2', css_class='ltr-form'),
			FormActions(
				Submit('submit', 'ثبت‌نام', css_class="bg-light-purple"),
			),
		)

	class Meta:
		model = User
		fields = [
			'username',
			'first_name',
			'last_name',
			'email',
			'password1',
			'password2'

		]

	def save(self, commit=True):
		user = super(SignupForm, self).save(commit=False)
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.email = self.cleaned_data['email']

		if commit:
			user.save()

		return user

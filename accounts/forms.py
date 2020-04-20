from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, HTML
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, UserChangeForm

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


class PasswordResetConfirmForm(SetPasswordForm):
	def __init__(self, user, *args, **kwargs):
		super().__init__(user, *args, **kwargs)
		self.fields['new_password1'].help_text = None


class EditProfileForm(UserChangeForm):
	# Suppress help texts
	def __init__(self, *args, **kwargs):
		super(UserChangeForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_class = 'form-horizontal col-md-10 mx-auto'
		self.helper.label_class = 'col-lg-12'
		self.helper.field_class = 'col'
		self.helper.use_custom_control = True
		self.helper.layout = Layout(
			Div('first_name', css_class='col'),
			Div('last_name', css_class='col'),
			Div('university', css_class='col'),
			Div('major', css_class='col'),
			Div('bio', css_class='col'),
			Div('profile_picture', css_class='col'),
			FormActions(
				Submit('submit', 'به روزرسانی', css_class="bg-light-purple"),
			),
		)

	class Meta:
		model = User
		fields = [
			'first_name',
			'last_name',
			'university',
			'major',
			'bio',
			'profile_picture',
		]

	def save(self, commit=True):
		user = super(UserChangeForm, self).save(commit=False)
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.bio = self.cleaned_data['bio']
		user.university = self.cleaned_data['university']
		user.major = self.cleaned_data['major']

		# If new image has been selected, set it to that image
		# Else set to default profile_picture
		if 'profile_picture' in self.files:
			user.profile_picture = self.files['profile_picture']
		else:
			user.profile_picture = 'default_profile_picture.png'

		if commit:
			user.save()

		return user

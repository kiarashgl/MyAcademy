from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, HTML

from django.forms import ModelForm
from .models import Professor, Department, University


class ProfessorForm(ModelForm):

	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)
		self.fields['my_department'].queryset = Department.objects.filter(verified=True)

		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_class = 'form-horizontal col-md-10 mx-auto'
		self.helper.label_class = 'col-lg-12'
		self.helper.field_class = 'col'
		self.helper.use_custom_control = True
		self.helper.layout = Layout(
			Div(
				Div('first_name', css_class='col'),
				Div('last_name', css_class='col'),
				css_class='row'
			),
			Div('my_department', css_class='ltr-form'),
			FormActions(
				Submit('submit', 'ثبت', css_class="bg-light-purple"),
			),
		)

	class Meta:
		model = Professor
		fields = ['first_name', 'last_name', 'my_department']


class DepartmentForm(ModelForm):

	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)
		self.fields['my_university'].queryset = University.objects.filter(verified=True)

		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_class = 'form-horizontal col-md-10 mx-auto'
		self.helper.label_class = 'col-lg-12'
		self.helper.field_class = 'col'
		self.helper.use_custom_control = True
		self.helper.layout = Layout(
			Div('name', css_class='col'),
			Div('my_university', css_class='ltr-form'),
			FormActions(
				Submit('submit', 'ثبت', css_class="bg-light-purple"),
			),
		)

	class Meta:
		model = Department
		fields = ['name', 'my_university']


class UniversityForm(ModelForm):

	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_class = 'form-horizontal col-md-10 mx-auto'
		self.helper.label_class = 'col-lg-12'
		self.helper.field_class = 'col'
		self.helper.use_custom_control = True
		self.helper.layout = Layout(
			Div('name', css_class='col'),
			Div('address', css_class='ltr-form'),
			FormActions(
				Submit('submit', 'ثبت', css_class="bg-light-purple"),
			),
		)

	class Meta:
		model = University
		fields = ['name', 'address']

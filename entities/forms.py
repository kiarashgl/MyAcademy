from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, HTML

from django.forms import ModelForm
from django.urls import reverse, reverse_lazy

from .models import Professor, Department, University
from dal import autocomplete


class ProfessorForm(ModelForm):

	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)
		self.fields['my_department'].queryset = Department.objects.filter(verified=True)
		self.fields['my_department'].label_from_instance = lambda obj: f'{obj.name} - {obj.my_university}'
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
			Div(
				Div('rank', css_class='ltr-form'),
			),
			Div('my_department', css_class='ltr-form'),
			FormActions(
				Submit('submit', 'ثبت', css_class="bg-light-purple"),
			),
		)

	class Meta:
		model = Professor
		fields = ['first_name', 'last_name', 'rank', 'my_department']
		widgets = {
			'my_department': autocomplete.ModelSelect2(url=reverse_lazy('entities:department_autocomplete')),
		}


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
			Div('my_university', css_class='col'),
			FormActions(
				Submit('submit', 'ثبت', css_class="bg-light-purple"),
			),
		)

	class Meta:
		model = Department
		fields = ['name', 'my_university']

		widgets = {
			'my_university': autocomplete.ModelSelect2(url=reverse_lazy('entities:university_autocomplete')),
		}


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
			Div('address', css_class='col'),
			FormActions(
				Submit('submit', 'ثبت', css_class="bg-light-purple"),
			),
		)

	class Meta:
		model = University
		fields = ['name', 'address']

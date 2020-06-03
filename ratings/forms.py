from django.forms import ModelForm, Textarea
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from .models import ProfRating, DeptRating, UniRating


class RatingForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.add_input(Submit('submit', 'ثبت', css_class='bg-light-purple'))
		self.helper.form_method = 'POST'
		self.fields['comment'].widget = Textarea(attrs={'placeholder': 'اختیاری'})
		self.helper.layout = Layout(
			*[Field(field_name) for field_name in self.fields if field_name != 'comment'],
			Field('comment')
		)

	class Meta:
		abstract = True


class ProfRatingForm(RatingForm):
	class Meta:
		model = ProfRating
		exclude = ['user', 'prof']
		labels = {
			'take_course_suggestion': 'چه‌قدر برداشتن درس با این استاد را پیشنهاد می‌کنید؟',
			'research_suggestion': 'چه‌قدر انجام کار پژوهشی با این استاد را پیشنهاد می‌کنید؟',
		}


class DeptRatingForm(RatingForm):
	class Meta:
		model = DeptRating
		exclude = ['user', 'dept']


class UniRatingForm(RatingForm):
	class Meta:
		model = UniRating
		exclude = ['user', 'uni']

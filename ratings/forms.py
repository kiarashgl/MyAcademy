from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import ProfRating, DeptRating, UniRating


class RatingForm(ModelForm):
	helper = FormHelper()
	helper.add_input(Submit('submit', 'ثبت', css_class='bg-light-purple'))
	helper.form_method = 'POST'

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

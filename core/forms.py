from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout
from django.urls import reverse_lazy

from django.forms import Form, CharField, ChoiceField, RadioSelect, TextInput


class SearchForm(Form):
	q = CharField(label='جست‌وجو', widget=TextInput(attrs={'placeholder': 'مثال: دانشگاه صنعتی شریف', 'class': 'mainSearch'}),
				  max_length=100)

	filter_by = ChoiceField(label='میان', initial='all',
							widget=RadioSelect,
							choices=(('all', 'همه'), ('profs', 'اساتید'),
									 ('deps', 'دانشکده‌ها'),
									 ('unis', 'دانشگاه‌ها')))

	def __init__(self, *args, **kwargs):
		super(Form, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'GET'
		self.helper.form_class = 'no-asterisk'
		self.helper.form_action = reverse_lazy('entities:search_results')
		self.helper.disable_csrf = True
		self.helper.layout = Layout(
			Div('q'),
			Div(InlineRadios('filter_by'))
		)

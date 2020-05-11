from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper

from core.forms import SearchForm


class HomepageView(FormView):
	template_name = 'index.html'
	form_class = SearchForm

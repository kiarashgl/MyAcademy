from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, ListView, FormView
from .models import Professor, Department, University, Entity
from .forms import ProfessorForm, DepartmentForm, UniversityForm
from core.forms import SearchForm
from django.db.models import Q, F, Value as V
from django.db.models import Avg
from django.db.models.functions import Concat
from ratings.models import *


# Create your views here.

class EntityDetail(DetailView):

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['entity'] = self.object
		return context

	class Meta:
		abstract = True


class ProfessorDetail(EntityDetail):
	template_name = 'entities/professor_detail.html'
	queryset = Professor.objects.filter(verified=True)
	model = Professor


class DepartmentDetail(EntityDetail):
	template_name = 'entities/department_detail.html'
	queryset = Department.objects.filter(verified=True)
	model = Department


class UniversityDetail(EntityDetail):
	template_name = 'entities/university_detail.html'
	queryset = University.objects.filter(verified=True)
	model = University


class EntitySuggest(LoginRequiredMixin, SuccessMessageMixin, CreateView):
	login_url = reverse_lazy('accounts:login')
	success_url = reverse_lazy('home')

	class Meta:
		abstract = True


class ProfessorSuggest(EntitySuggest):
	template_name = 'entities/professor_suggest.html'
	form_class = ProfessorForm
	success_message = "استاد با موفقیت پیشنهاد داده شد."


class DepartmentSuggest(EntitySuggest):
	template_name = 'entities/department_suggest.html'
	form_class = DepartmentForm
	success_message = "دانشکده با موفقیت پیشنهاد داده شد."


class UniversitySuggest(EntitySuggest):
	template_name = 'entities/university_suggest.html'
	form_class = UniversityForm
	success_message = "دانشگاه با موفقیت پیشنهاد داده شد."


class ProfessorList(ListView):
	template_name = 'entities/professor_list.html'

	def get_queryset(self):
		return Professor.objects.filter(verified=True)


class DepartmentList(ListView):
	template_name = 'entities/department_list.html'

	def get_queryset(self):
		return Department.objects.filter(verified=True)


class UniversityList(ListView):
	template_name = 'entities/university_list.html'

	def get_queryset(self):
		return University.objects.filter(verified=True)


class SearchResultsView(FormView, ListView):
	template_name = 'entities/search_results.html'
	form_class = SearchForm

	def get_queryset(self):
		query = self.request.GET.get('q')
		filter_by = self.request.GET.get('filter_by')
		filter_by = filter_by if filter_by is not None else 'all'

		if filter_by == 'all' or filter_by == 'profs':
			profs = Professor.objects.annotate(
				full_name=Concat('first_name', V(' '), 'last_name')).filter(
				Q(full_name__icontains=query),
				verified=True
			)
		else:
			profs = Professor.objects.none()

		if filter_by == 'all' or filter_by == 'deps':
			deps = Department.objects.filter(
				Q(name__icontains=query),
				verified=True
			)
		else:
			deps = Department.objects.none()

		if filter_by == 'all' or filter_by == 'unis':
			unis = University.objects.filter(
				Q(name__icontains=query),
				verified=True
			)
		else:
			unis = University.objects.none()

		return list(profs) + list(deps) + list(unis)

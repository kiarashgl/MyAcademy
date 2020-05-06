from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, ListView, FormView
from .models import Professor, Department, University, Entity
from .forms import ProfessorForm, DepartmentForm, UniversityForm
from core.forms import SearchForm
from django.db.models import Q, F, Value as V
from django.db.models.functions import Concat


# Create your views here.


class ProfessorDetail(DetailView):
	template_name = 'entities/professor_detail.html'
	queryset = Professor.objects.filter(verified=True)
	model = Professor

	def get(self, request, **kwargs):
		try:
			self.model.objects.get(pk=kwargs['pk'])
			return super(DetailView, self).get(request, **kwargs)
		except self.model.DoesNotExist:
			return redirect(reverse_lazy('home'))


class DepartmentDetail(DetailView):
	template_name = 'entities/department_detail.html'
	queryset = Department.objects.filter(verified=True)
	model = Department

	def get(self, request, **kwargs):
		try:
			self.model.objects.get(pk=kwargs['pk'])
			return super(DetailView, self).get(request, **kwargs)
		except self.model.DoesNotExist:
			return redirect(reverse_lazy('home'))


class UniversityDetail(DetailView):
	template_name = 'entities/university_detail.html'
	queryset = University.objects.filter(verified=True)
	model = University

	def get(self, request, **kwargs):
		try:
			self.model.objects.get(pk=kwargs['pk'])
			return super(DetailView, self).get(request, **kwargs)
		except self.model.DoesNotExist:
			return redirect(reverse_lazy('home'))


class ProfessorSuggest(CreateView):
	template_name = 'entities/professor_suggest.html'
	form_class = ProfessorForm
	success_url = reverse_lazy('home')


class DepartmentSuggest(CreateView):
	template_name = 'entities/department_suggest.html'
	form_class = DepartmentForm
	success_url = reverse_lazy('home')


class UniversitySuggest(CreateView):
	template_name = 'entities/university_suggest.html'
	form_class = UniversityForm
	success_url = reverse_lazy('home')


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

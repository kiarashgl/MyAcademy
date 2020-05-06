from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, ListView
from .models import Professor, Department, University, Entity
from .forms import ProfessorForm, DepartmentForm, UniversityForm
from django.db.models import Q, F


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


class SearchResultsView(ListView):
	template_name = 'entities/search_results.html'

	def get_queryset(self):
		query = self.request.GET.get('q')

		print(query)

		profs = Professor.objects.all().filter(
			Q(first_name__icontains=query) | Q(last_name__icontains=query),
			# TODO: Moos fix this (Make it search on first_name + " " + last_name instead of searching on them one by one
			verified=True
		)

		deps = Department.objects.filter(
			Q(name__icontains=query),
			verified=True
		)

		unis = University.objects.filter(
			Q(name__icontains=query),
			verified=True
		)

		return list(profs) + list(deps) + list(unis)

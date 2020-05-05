from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import DetailView
from .models import Professor, Department, University


# Create your views here.

def template(request):
	return HttpResponse("<h1> HI </h1>")


class ProfessorDetail(DetailView):
	template_name = 'entities/professor_detail.html'
	queryset = Professor.objects.filter(verified=True)
	model = Professor


class DepartmentDetail(DetailView):
	template_name = 'entities/department_detail.html'
	queryset = Department.objects.filter(verified=True)
	model = Department


class UniversityDetail(DetailView):
	template_name = 'entities/university_detail.html'
	queryset = University.objects.filter(verified=True)
	model = University

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from entities.models import Professor, Department, University
from .models import ProfRating, DeptRating, UniRating
from .forms import ProfRatingForm, DeptRatingForm, UniRatingForm


class EntityRatingView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
	login_url = reverse_lazy('accounts:login')
	success_url = reverse_lazy('home')
	sucess_message = 'امتیازدهی شما با موفقیت ثبت شد.'

	def get_object(self, queryset=None):
		if queryset.exists():
			return queryset.first()
		else:
			return None

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

	class Meta:
		abstract = True


class ProfRatingView(EntityRatingView):
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['entity_name'] = self.object.prof.name
		return context

	def get_object(self, queryset=None):
		queryset = ProfRating.objects.filter(user=self.request.user, prof=self.kwargs['pk'])
		return super().get_object(queryset)

	def form_valid(self, form):
		form.instance.prof = Professor.objects.get(pk=self.kwargs['pk'])
		return super().form_valid(form)

	template_name = 'rating.html'
	form_class = ProfRatingForm	
	model = ProfRating


class DeptRatingView(EntityRatingView):
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['entity_name'] = self.object.dept.name
		return context

	def get_object(self, queryset=None):
		queryset = DeptRating.objects.filter(user=self.request.user, dept=self.kwargs['pk'])
		return super().get_object(queryset)

	def form_valid(self, form):
		form.instance.dept = Department.objects.get(pk=self.kwargs['pk'])
		return super().form_valid(form)

	template_name = 'rating.html'
	form_class = DeptRatingForm
	model = DeptRating


class UniRatingView(EntityRatingView):
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['entity_name'] = self.object.uni.name
		return context

	def get_object(self, queryset=None):
		queryset = UniRating.objects.filter(user=self.request.user, uni=self.kwargs['pk'])
		return super().get_object(queryset)

	def form_valid(self, form):
		form.instance.uni = University.objects.get(pk=self.kwargs['pk'])
		return super().form_valid(form)

	template_name = 'rating.html'
	form_class = UniRatingForm
	model = UniRating

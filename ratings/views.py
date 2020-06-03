from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from entities.models import Professor, Department, University
from .models import ProfRating, DeptRating, UniRating, RatingField
from .forms import ProfRatingForm, DeptRatingForm, UniRatingForm

from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from django.db.models import Avg, Count, Max, Min, Q


class EntityRatingView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
	login_url = reverse_lazy('accounts:login')
	success_url = reverse_lazy('home')
	success_message = 'امتیازدهی شما با موفقیت ثبت شد.'

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
		context['entity_name'] = Professor.objects.get(pk=self.kwargs['pk']).name
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
		context['entity_name'] = Department.objects.get(pk=self.kwargs['pk']).name
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
		context['entity_name'] = University.objects.get(pk=self.kwargs['pk']).name
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


class ProfessorRatingData(APIView):
	queryset = ProfRating.objects.all()

	def get(self, request, pk):
		query = ProfRating.objects.filter(prof=pk)

		data = {}
		if query.exists():
			# General questions
			fields = [x for x in ProfRating._meta.get_fields() if isinstance(x, RatingField)]
			avg_fields_dict = {x.name: Avg(x.name) for x in fields}
			count_fields_dict = {}
			for i in range(1, 6):
				for x in fields:
					count_fields_dict['%s_%s' % (x.name, i)] = Count(x.name, filter=Q(**{x.name: i}))

			averages = query.aggregate(**avg_fields_dict)
			counts = query.aggregate(**count_fields_dict)

			general_fields = [x for x in fields if x.name in ['knowledge', 'attention', 'order', 'manners']]
			general_fields[1], general_fields[3] = general_fields[3], general_fields[1]

			general_labels = [x.verbose_name for x in general_fields]
			general_data = [averages[x.name] for x in general_fields]
			general = {
				"title": "کلیات",
				"labels": general_labels,
				"data": general_data
			}

			teaching_fields = [x for x in fields if x.name in ['teaching', 'grading', 'load', 'interesting']]
			teaching_labels = [x.verbose_name for x in teaching_fields]
			teaching_data = [averages[x.name] for x in teaching_fields]
			teaching = {
				"title": "آموزش",
				"labels": teaching_labels,
				"data": teaching_data
			}

			count_labels = ["%s / 5" % i for i in range(1, 6)]
			research_data = [counts['research_%s' % i] for i in range(1, 6)]
			advice_data = [counts['advice_%s' % i] for i in range(1, 6)]
			research = {
				"research": {"data": research_data, "label": "توانایی در کارهای پژوهشی"},
				"advice": {"data": advice_data, "label": "راهنمایی‌های مفید"},
				"labels": count_labels,
				"title": "پژوهش",
			}

			overall_scores = {
				"class_score": averages['take_course_suggestion'],
				"research_score": averages["research_suggestion"],
			}

			data['general'] = general
			data['teaching'] = teaching
			data['research'] = research

			data['overall'] = overall_scores

		return Response(data)


class DepartmentRatingData(APIView):
	queryset = DeptRating.objects.all()

	def get(self, request, pk):
		query = DeptRating.objects.filter(dept=pk)

		data = {}
		if query.exists():
			# General questions

			fields = [x for x in DeptRating._meta.get_fields() if isinstance(x, RatingField)]
			avg_fields_dict = {x.name: Avg(x.name) for x in fields}
			averages = query.aggregate(**avg_fields_dict)

			labels = [x.verbose_name for x in fields]
			avg_data = [averages[x.name] for x in fields]

			data = {
				"labels": labels,
				"data": avg_data,
				"title": "میانگین امتیاز ها"
			}

		return Response(data)


class UniversityRatingData(APIView):
	queryset = UniRating.objects.all()

	def get(self, request, pk):
		query = UniRating.objects.filter(uni=pk)

		data = {}
		if query.exists():
			# General questions

			fields = [x for x in UniRating._meta.get_fields() if isinstance(x, RatingField)]
			avg_fields_dict = {x.name: Avg(x.name) for x in fields}
			averages = query.aggregate(**avg_fields_dict)

			labels = [x.verbose_name for x in fields]
			avg_data = [averages[x.name] for x in fields]

			data = {
				"labels": labels,
				"data": avg_data,
				"title": "میانگین امتیاز ها"
			}

		return Response(data)

from django.urls import path, include
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetCompleteView
from . import views

app_name = 'entities'
urlpatterns = [
	path('professor/<int:pk>', views.ProfessorDetail.as_view(), name='professor_detail'),
	path('department/<int:pk>', views.DepartmentDetail.as_view(), name='department_detail'),
	path('university/<int:pk>', views.UniversityDetail.as_view(), name='university_detail'),

	path('professor/suggest', views.ProfessorSuggest.as_view(), name='professor_suggest'),
	path('department/suggest', views.DepartmentSuggest.as_view(), name='department_suggest'),
	path('university/suggest', views.UniversitySuggest.as_view(), name='university_suggest'),

	path('search', views.SearchResultsView.as_view(), name='search_results'),
]

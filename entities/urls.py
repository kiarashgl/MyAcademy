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

	path('professor/all', views.ProfessorList.as_view(), name='professor_all'),
	path('department/all', views.DepartmentList.as_view(), name='department_all'),
	path('university/all', views.UniversityList.as_view(), name='university_all'),

	path('search', views.SearchResultsView.as_view(), name='search_results'),

	path('autocomplete', views.entity_autocomplete, name='entity_autocomplete'),
	path('university-autocomplete', views.UniversityAutocomplete.as_view(), name='university_autocomplete'),
	path('department-autocomplete', views.DepartmentAutocomplete.as_view(), name='department_autocomplete'),
	path('professor-autocomplete', views.ProfessorAutocomplete.as_view(), name='professor_autocomplete'),

]

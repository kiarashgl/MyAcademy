from django.urls import path, include
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetCompleteView
from . import views

app_name = 'entities'
urlpatterns = [
	path('', views.template),
	path('professor/<int:pk>', views.ProfessorDetail.as_view()),
	path('department/<int:pk>', views.DepartmentDetail.as_view()),
	path('university/<int:pk>', views.UniversityDetail.as_view()),
]

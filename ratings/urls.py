from django.urls import path
from . import views

app_name = 'ratings'
urlpatterns = [
	path('professor/<int:pk>', views.ProfRatingView.as_view(), name='professor_rating'),
	path('department/<int:pk>', views.DeptRatingView.as_view(), name='department_rating'),
	path('university/<int:pk>', views.UniRatingView.as_view(), name='university_rating'),

	path('api/professor/<int:pk>', views.ProfessorRatingData.as_view(), name='professor_rating_data'),
	path('api/department/<int:pk>', views.DepartmentRatingData.as_view(), name='department_rating_data'),
	path('api/university/<int:pk>', views.UniversityRatingData.as_view(), name='university_rating_data'),

]

from django.urls import path
from . import views


app_name = 'ratings'
urlpatterns = [
	path('professor/<int:pk>', views.ProfRatingView.as_view(), name='professor_rating'),
	path('department/<int:pk>', views.DeptRatingView.as_view(), name='department_rating'),
	path('university/<int:pk>', views.UniRatingView.as_view(), name='university_rating'),
]

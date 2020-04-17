from django.urls import path, include
from . import views

app_name = 'accounts'
urlpatterns = [
	path('login/', views.Login.as_view(), name='login'),
	path('signup/', views.SignUp.as_view(), name='signup'),
	path('', include('django.contrib.auth.urls')),
]

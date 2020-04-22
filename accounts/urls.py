from django.urls import path, include
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetCompleteView
from . import views

app_name = 'accounts'
urlpatterns = [
	path('login/', views.Login.as_view(), name='login'),


	path('signup/', views.SignUp.as_view(), name='signup'),

	path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
	path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),

	path('reset/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
	path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

	path('profile/', views.Profile.as_view(), name='profile'),
	path('profile/edit/', views.EditProfile.as_view(), name='profile_edit'),

	path('', include('django.contrib.auth.urls')),
]

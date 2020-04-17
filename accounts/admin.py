from django.contrib import admin
from django.contrib.auth import get_user_model
import django.contrib.auth.admin

from .forms import SignupForm
from .models import User

admin.site.register(User)

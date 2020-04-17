from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	email = models.EmailField(max_length=100)
	username = models.CharField(max_length=100, unique=True)
	password = models.CharField(max_length=50)
	is_moderator = models.BooleanField(default=False)

	def __str__(self):
		return self.username

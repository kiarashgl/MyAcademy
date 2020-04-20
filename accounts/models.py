from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext as _


class User(AbstractUser):
	# Authentication fields
	first_name = models.CharField(_('first name'), max_length=30, blank=False)
	last_name = models.CharField(_('last name'), max_length=30, blank=False)
	email = models.EmailField(_('email address'), max_length=100, blank=False)
	REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

	# Extra profile fields
	profile_picture = models.ImageField(upload_to='profile_pictures', default='default_profile_picture.png')
	bio = models.CharField(max_length=100, blank=True)
	university = models.CharField(max_length=100, blank=True)
	major = models.CharField(max_length=100, blank=True)

	def __str__(self):
		return self.username

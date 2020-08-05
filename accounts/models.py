from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _

import hashlib

IDENTICON_API_URL = "https://identicon-api.herokuapp.com/%s/512?format=png"


class User(AbstractUser):
	# Authentication fields

	first_name = models.CharField(_('first name'), max_length=30, blank=False)
	last_name = models.CharField(_('last name'), max_length=30, blank=False)
	email = models.EmailField(_('email address'), max_length=100, blank=False)
	REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

	# Extra profile fields
	profile_picture = models.ImageField("تصویر نمایه", upload_to='profile_pictures',
										null=True, blank=True)
	bio = models.TextField("بیوگرافی", blank=True)
	university = models.CharField("دانشگاه", max_length=100, blank=True)
	major = models.CharField("رشته", max_length=100, blank=True, )

	def __str__(self):
		return self.username

	@property
	def get_profile_picture_url(self):
		try:
			if self.profile_picture is not None:
				return self.profile_picture.url
		except Exception:
			return IDENTICON_API_URL % (hashlib.md5(self.username.encode('utf-8')).hexdigest())

		return IDENTICON_API_URL % (hashlib.md5(self.username.encode('utf-8')).hexdigest())


@receiver(post_save, sender=User)
def add_to_blog_editors(sender, instance, created, **kwargs):
	if created:
		instance.groups.add(Group.objects.get(name='Editors'))

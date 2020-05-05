from django.db import models


class Entity(models.Model):
	verified = models.BooleanField(default=False)
	picture = models.ImageField(upload_to='profile_pictures', null=True)

	def __str__(self):
		raise NotImplementedError


class Professor(Entity):
	first_name = models.CharField(max_length=30, blank=False)
	last_name = models.CharField(max_length=30, blank=False)
	my_department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)

	# tags = None # TODO: Fix later

	def __str__(self):
		return self.first_name + " " + self.last_name


class Department(Entity):
	name = models.CharField(max_length=30, blank=False)
	my_university = models.ForeignKey('University', on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.name


class University(Entity):
	name = models.CharField(max_length=30, blank=False)
	address = models.CharField(max_length=100, blank=True)  # TODO: Fix later

	def __str__(self):
		return self.name

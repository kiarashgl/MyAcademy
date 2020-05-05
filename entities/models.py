from django.db import models


class Entity(models.Model):
	verified = models.BooleanField(default=False)


class Professor(Entity):
	first_name = models.CharField(max_length=30, blank=False)
	last_name = models.CharField(max_length=30, blank=False)

	# picture = models.ImageField(upload_to='profile_pictures', default='default_profile_picture.png') # TODO: Will do later

	department_name = models.CharField(max_length=30,
	                                   blank=True)  # TODO: Fix later and add in a reference to a department
	university_name = models.CharField(max_length=30,
	                                   blank=True)  # TODO: Fix later and add in a reference to a university

	score = models.IntegerField()  # Between 0-10 # TODO: Fix later (Must be computed or some shit in the next sprints)
	# tags = None # TODO: Fix later
	pass

	def __str__(self):
		return self.first_name + " " + self.last_name


class Department(Entity):
	name = models.CharField(max_length=30, blank=False)
	university_name = models.CharField(max_length=30,
	                                   blank=False)  # TODO: Fix later and add in a reference to a university

	score = models.IntegerField()  # Between 0-10 # TODO: Fix later (Must be computed or some shit in the next sprints)

	def __str__(self):
		return self.name


class University(Entity):
	name = models.CharField(max_length=30, blank=False)
	address = models.CharField(max_length=100, blank=True)  # TODO: Fix later

	def __str__(self):
		return self.name

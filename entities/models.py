from django.db import models
from django.utils.translation import ugettext_lazy as _


class Entity(models.Model):
	verified = models.BooleanField(default=False)
	picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)

	class Meta:
		abstract = True


class Professor(Entity):
	first_name = models.CharField(max_length=30, blank=False)
	last_name = models.CharField(max_length=30, blank=False)
	my_department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.first_name + " " + self.last_name

	class Meta:
		verbose_name = _("استاد")
		verbose_name_plural = _("اساتید")


class Department(Entity):
	name = models.CharField(max_length=30, blank=False)
	my_university = models.ForeignKey('University', on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = _("دپارتمان")
		verbose_name_plural = _("دپارتمان ها")


class University(Entity):
	name = models.CharField(max_length=30, blank=False)
	address = models.CharField(max_length=100, blank=True)  # TODO: Fix later

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = _("دانشگاه")
		verbose_name_plural = _("دانشگاه ها")

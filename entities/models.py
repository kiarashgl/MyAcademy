from django.db import models
from django.utils.translation import ugettext_lazy as _

from MyAcademy.settings import MEDIA_URL


class Entity(models.Model):
	verified = models.BooleanField(default=False)
	picture = models.ImageField(upload_to='profile_pictures', blank=True)

	@property
	def get_picture(self):
		if (self.picture):
			return self.picture.url
		else:
			return MEDIA_URL + self._meta.get_field('picture').default

	class Meta:
		abstract = True


class Professor(Entity):
	INSTRUCTOR = 'ins'
	ASSISTANT = 'asi'
	ASSOCIATE = 'aso'
	FULL = 'ful'
	ACADEMIC_RANK = [
		(INSTRUCTOR, 'مدرس'),
		(ASSISTANT, 'استادیار'),
		(ASSOCIATE, 'دانشیار'),
		(FULL, 'استاد'),
	]

	first_name = models.CharField(_("first name"), max_length=30, blank=False)
	last_name = models.CharField(_("last name"), max_length=30, blank=False)
	my_department = models.ForeignKey('Department', verbose_name="نام دانشکده", on_delete=models.SET_NULL, null=True)
	rank = models.CharField(max_length=3, choices=ACADEMIC_RANK, verbose_name="مرتبه‌ی علمی", default=INSTRUCTOR)

	@property
	def name(self):
		return self.first_name + " " + self.last_name

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._meta.get_field('picture').default ='/profile_pictures/professor_default_picture.png'

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = _("استاد")
		verbose_name_plural = _("اساتید")
		constraints = [
			models.UniqueConstraint(fields=['first_name', 'last_name', 'my_department'], name='unique_professor'),
		]


class Department(Entity):
	name = models.CharField(_("name"), max_length=30, blank=False)
	my_university = models.ForeignKey('University', verbose_name="دانشکده", on_delete=models.SET_NULL, null=True)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._meta.get_field('picture').default ='/profile_pictures/department_default_picture.png'

	def __str__(self):
		return self.name

	@property
	def professors(self):
		return Professor.objects.filter(my_department=self)


	class Meta:
		verbose_name = _("دانشکده")
		verbose_name_plural = _("دانشکده‌ها")
		constraints = [
			models.UniqueConstraint(fields=['name', 'my_university'], name='unique_department'),
		]


class University(Entity):
	name = models.CharField(_("name"), max_length=30, blank=False, unique=True)
	address = models.CharField("آدرس", max_length=100, blank=True)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._meta.get_field('picture').default ='/profile_pictures/university_default_picture.png'

	def __str__(self):
		return self.name

	@property
	def departments(self):
		return Department.objects.filter(my_university=self)

	class Meta:
		verbose_name = _("دانشگاه")
		verbose_name_plural = _("دانشگاه‌ها")
from django.db import models
from django.urls import reverse_lazy

from .widgets import RatingStars
from MyAcademy.settings import AUTH_USER_MODEL


class RatingReaction(models.Model):
	user = models.ForeignKey('accounts.User', verbose_name='کاربر', on_delete=models.CASCADE)
	is_like = models.BooleanField()

	class Meta:
		abstract = True


class ProfRatingReaction(RatingReaction):
	rating = models.ForeignKey('ProfRating', verbose_name='نظر', on_delete=models.CASCADE)

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['user', 'rating'], name='unique_profcomment_like'),
		]


class DeptRatingReaction(RatingReaction):
	rating = models.ForeignKey('DeptRating', verbose_name='نظر', on_delete=models.CASCADE)

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['user', 'rating'], name='unique_deptcomment_like'),
		]


class UniRatingReaction(RatingReaction):
	rating = models.ForeignKey('UniRating', verbose_name='نظر', on_delete=models.CASCADE)

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['user', 'rating'], name='unique_unicomment_like'),
		]


class RatingField(models.IntegerField):
	ONE_TO_FIVE_RATING_CHOICES = (
		(1, '1'),
		(2, '2'),
		(3, '3'),
		(4, '4'),
		(5, '5'),
	)

	def __init__(self, *args, **kwargs):
		kwargs['choices'] = RatingField.ONE_TO_FIVE_RATING_CHOICES
		kwargs['null'] = True
		super().__init__(*args, **kwargs)

	def formfield(self, **kwargs):
		kwargs['widget'] = RatingStars(stars=len(RatingField.ONE_TO_FIVE_RATING_CHOICES))
		return super(models.IntegerField, self).formfield(**kwargs)


class Rating(models.Model):
	user = models.ForeignKey(AUTH_USER_MODEL, verbose_name='کاربر', on_delete=models.CASCADE)
	comment = models.TextField(verbose_name='نظر', blank=True)
	date = models.DateField(auto_now=True, verbose_name='تاریخ')

	# https://docs.djangoproject.com/en/dev/topics/db/models/#be-careful-with-related-name
	liked_users = models.ManyToManyField(AUTH_USER_MODEL,
										 blank=True,
										 related_name='%(app_label)s_%(class)s_likes')
	disliked_users = models.ManyToManyField(AUTH_USER_MODEL,
											blank=True,
											related_name='%(app_label)s_%(class)s_dislikes')

	@property
	def get_like_url(self):
		return reverse_lazy('ratings:comment_like', kwargs={"pk": self.pk})

	@property
	def get_dislike_url(self):
		return reverse_lazy('ratings:comment_dislike', kwargs={"pk": self.pk})

	class Meta:
		abstract = True


class ProfRating(Rating):
	prof = models.ForeignKey('entities.Professor', verbose_name='استاد', on_delete=models.CASCADE)

	# general questions
	knowledge = RatingField(verbose_name='دانش و تخصص')
	manners = RatingField(verbose_name='اخلاق')
	order = RatingField(verbose_name='نظم و بابرنامگی')
	attention = RatingField(verbose_name='توجه به دانشجو')

	# teaching questions
	teaching = RatingField(verbose_name='کیفیت تدریس', blank=True)
	grading = RatingField(verbose_name='نمره‌دهی', blank=True)
	load = RatingField(verbose_name='حجم تمارین و پروژه‌ها', blank=True)
	interesting = RatingField(verbose_name='جذابیت کلاس', blank=True)

	# research questions
	research = RatingField(verbose_name='توانایی در کارهای پژوهشی', blank=True)
	advice = RatingField(verbose_name='راهنمایی‌های مفید', blank=True)

	take_course_suggestion = RatingField(blank=True)
	research_suggestion = RatingField(blank=True)

	class Meta:
		verbose_name = 'امتیاز استاد'
		verbose_name_plural = 'امتیازهای اساتید'
		constraints = [
			models.UniqueConstraint(fields=['user', 'prof'], name='unique_prof_rating'),
		]


class DeptRating(Rating):
	dept = models.ForeignKey('entities.Department', verbose_name='دانشکده', on_delete=models.CASCADE)

	teaching = RatingField(verbose_name='کیفیت آموزشی')
	research = RatingField(verbose_name='کیفیت پژوهشی')
	update = RatingField(verbose_name='اساتید به‌روز')
	industry = RatingField(verbose_name='ارتباط با صنعت')
	lab = RatingField(verbose_name='امکانات آزمایشگاهی')
	programs = RatingField(verbose_name='فوق برنامه')
	flexibility = RatingField(verbose_name='قوانین انعطاف پذیر')

	class Meta:
		verbose_name = 'امتیاز دانشکده'
		verbose_name_plural = 'امتیازهای دانشکده‌ها'
		constraints = [
			models.UniqueConstraint(fields=['user', 'dept'], name='unique_dept_rating'),
		]


class UniRating(Rating):
	uni = models.ForeignKey('entities.University', verbose_name='دانشگاه', on_delete=models.CASCADE)

	campus = RatingField(verbose_name='محیط')
	employment = RatingField(verbose_name='اشتغال فارغ‌التحصیلان')
	dorm = RatingField(verbose_name='خوابگاه')
	accessibility = RatingField(verbose_name='دسترسی آسان')
	programs = RatingField(verbose_name='فوق برنامه')
	leisure = RatingField(verbose_name='امکانات تفریحی')

	class Meta:
		verbose_name = 'امتیاز دانشگاه'
		verbose_name_plural = 'امتیازهای دانشگاه‌ها'
		constraints = [
			models.UniqueConstraint(fields=['user', 'uni'], name='unique_uni_rating'),
		]

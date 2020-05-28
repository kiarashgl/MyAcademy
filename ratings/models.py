from django.db import models


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


class Rating(models.Model):
	user = models.ForeignKey('accounts.User', verbose_name='کاربر', on_delete=models.CASCADE)

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
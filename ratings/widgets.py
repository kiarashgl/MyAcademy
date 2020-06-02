from django.forms import Widget


class RatingStars(Widget):
	template_name = 'rating_stars.html'

	def __init__(self, stars, attrs=None):
		super(RatingStars, self).__init__(attrs)
		self.stars = stars

	def get_context(self, name, value, attrs):
		context = super(RatingStars, self).get_context(name, value, attrs)
		context['stars'] = range(self.stars, 0, -1)
		return context

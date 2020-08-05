from django.db import models
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.db.models import Count

from modelcluster.fields import ParentalKey, ParentalManyToManyField

from wagtail.core.models import Page, Orderable
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import RichTextField, StreamField

from wagtail.core import blocks as core_blocks
from wagtail.images import blocks as image_blocks
from wagtail.images.fields import ImageField

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from MyAcademy.settings import BLOG_PAGINATION_PER_PAGE, DEBUG, AUTH_USER_MODEL


class CaptionedImageBlock(core_blocks.StructBlock):
	image = image_blocks.ImageChooserBlock(required=True)
	caption = core_blocks.CharBlock()


class BlogListingPage(Page):
	template = 'blog/home_page.html'

	body = RichTextField(blank=True)

	content_panels = Page.content_panels + [
		FieldPanel('body', classname="full"),
	]

	def get_context(self, request, *args, **kwargs):
		context = super(BlogListingPage, self).get_context(request)

		order = request.GET.get('orderby')

		if order == 'popular':
			all_posts = BlogDetailPage.objects.child_of(self).live().public() \
				.annotate(score=Count('liked_users') - Count('disliked_users')).order_by('-score')
		else:
			all_posts = BlogDetailPage.objects.child_of(self).live().public() \
				.order_by('-first_published_at')

		paginator = Paginator(all_posts, BLOG_PAGINATION_PER_PAGE)

		# Try to get the ?page=x value
		page = request.GET.get("page")
		try:
			# If the page exists and the ?page=x is an int
			posts = paginator.page(page)
		except PageNotAnInteger:
			# If the ?page=x is not an int; show the first page
			posts = paginator.page(1)
		except EmptyPage:
			# If the ?page=x is out of range (too high most likely)
			# Then return the last page
			posts = paginator.page(paginator.num_pages)

		context['posts'] = posts
		return context


class BlogDetailPage(RoutablePageMixin, Page):
	template = 'blog/blog_page.html'

	date = models.DateField("Post date", auto_now=True)
	intro = models.CharField(max_length=250)
	thumbnail = models.ForeignKey(
		'wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+'
	)

	body = StreamField([
		('heading', core_blocks.CharBlock(classname="full title")),
		('paragraph', core_blocks.RichTextBlock()),
		('image', image_blocks.ImageChooserBlock()),
		('image_slider', core_blocks.ListBlock(CaptionedImageBlock(), icon='image', label='Slider')),
	], blank=True)

	# https://docs.djangoproject.com/en/dev/topics/db/models/#be-careful-with-related-name
	liked_users = ParentalManyToManyField(AUTH_USER_MODEL,
										  blank=True,
										  related_name='%(app_label)s_%(class)s_likes')
	disliked_users = ParentalManyToManyField(AUTH_USER_MODEL,
											 blank=True,
											 related_name='%(app_label)s_%(class)s_dislikes')

	search_fields = Page.search_fields + [
		index.SearchField('intro'),
		index.SearchField('body'),
	]

	content_panels = Page.content_panels + [
		ImageChooserPanel('thumbnail'),
		FieldPanel('intro'),
		StreamFieldPanel('body'),
	]

	@property
	def likes(self):
		return self.liked_users.count()

	@property
	def dislikes(self):
		return self.disliked_users.count()

	def get_context(self, request, *args, **kwargs):
		context = super(BlogDetailPage, self).get_context(request)

		user = request.user
		context['liked'] = user in self.liked_users.all()
		context['likes'] = self.likes
		context['disliked'] = user in self.disliked_users.all()
		context['dislikes'] = self.dislikes

		return context

	# Needed for django-comments-xtd to work
	def get_absolute_url(self):
		if DEBUG:
			return 'http://localhost:8000' + self.url
		else:
			return self.full_url

	@route(r'^like/')
	def toggle_like(self, request):
		if request.is_ajax():
			user = request.user
			dislike_count_change = 0

			if user in self.disliked_users.all():
				self.disliked_users.remove(user)
				dislike_count_change = -1

			liked = False
			if user not in self.liked_users.all():
				self.liked_users.add(user)
				liked = True
				like_count_change = 1
			else:
				self.liked_users.remove(user)
				like_count_change = -1

			self.save()

			print(self.likes, self.dislikes)

			data = {
				'liked': liked,
				'like_count_change': like_count_change,
				'disliked': False,
				'dislike_count_change': dislike_count_change
			}

			return JsonResponse(data)
		else:
			return JsonResponse({})

	@route(r'^dislike/')
	def toggle_dislike(self, request):
		if request.is_ajax():
			user = request.user

			like_count_change = 0
			if user in self.liked_users.all():
				self.liked_users.remove(user)
				like_count_change = -1

			disliked = False
			if user not in self.disliked_users.all():
				self.disliked_users.add(user)
				disliked = True
				dislike_count_change = 1
			else:
				self.disliked_users.remove(user)
				dislike_count_change = -1

			self.save()
			print(self.likes, self.dislikes)

			data = {
				'liked': False,
				'like_count_change': like_count_change,
				'disliked': disliked,
				'dislike_count_change': dislike_count_change,
			}

			return JsonResponse(data)
		else:
			return JsonResponse({})

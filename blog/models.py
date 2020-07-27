from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField

from wagtail.core import blocks as core_blocks
from wagtail.images import blocks as image_blocks

from wagtail.images.fields import ImageField

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from MyAcademy.settings import BLOG_PAGINATION_PER_PAGE, DEBUG


class HomePage(Page):
	body = RichTextField(blank=True)

	content_panels = Page.content_panels + [
		FieldPanel('body', classname="full"),
	]

	def get_context(self, request, *args, **kwargs):
		context = super(HomePage, self).get_context(request)

		all_posts = self.get_children().live().public().order_by('-first_published_at')

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


class BlogPage(Page):
	date = models.DateField("Post date")
	intro = models.CharField(max_length=250)
	thumbnail = models.ForeignKey(
		'wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+'
	)

	body = RichTextField(blank=True)

	search_fields = Page.search_fields + [
		index.SearchField('intro'),
		index.SearchField('body'),
	]

	content_panels = Page.content_panels + [
		ImageChooserPanel('thumbnail'),

		FieldPanel('date'),
		FieldPanel('intro'),

		FieldPanel('body', classname="full"),
		InlinePanel('gallery_images', label="Gallery images"),
	]

	def get_absolute_url(self):
		if DEBUG:
			return 'http://localhost:8000' + self.url
		else:
			return self.full_url


class AdvancedBlogPage(Page):
	date = models.DateField("Post date")
	intro = models.CharField(max_length=250)
	thumbnail = models.ForeignKey(
		'wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+'
	)

	body = StreamField([
		('heading', core_blocks.CharBlock(classname="full title")),
		('paragraph', core_blocks.RichTextBlock()),
		('image', image_blocks.ImageChooserBlock()),
		('image_slider', core_blocks.ListBlock(image_blocks.ImageChooserBlock(), icon='image', label='Slider')),
	])

	search_fields = Page.search_fields + [
		index.SearchField('intro'),
		index.SearchField('body'),
	]

	content_panels = Page.content_panels + [
		ImageChooserPanel('thumbnail'),

		FieldPanel('date'),
		FieldPanel('intro'),

		StreamFieldPanel('body'),
	]

	def get_absolute_url(self):
		if DEBUG:
			return 'http://localhost:8000' + self.url
		else:
			return self.full_url


class BlogPageGalleryImage(Orderable):
	page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
	image = models.ForeignKey(
		'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
	)
	caption = models.CharField(blank=True, max_length=250)

	panels = [
		ImageChooserPanel('image'),
		FieldPanel('caption'),
	]

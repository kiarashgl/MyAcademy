from django.test import TestCase
from wagtail.tests.utils import WagtailPageTests
from wagtail.tests.utils.form_data import nested_form_data, streamfield

from blog.models import BlogListingPage, BlogDetailPage
from accounts.models import User
from django.urls import reverse

from MyAcademy import settings


class BlogPanelTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		User.objects.create_user(username='mamad', first_name='ممد', last_name='ممدی',
								 email='mamad@mamadi.ir', 
								 password='yY3Kky4Rz1S31v')
		settings.DISABLE_RECAPTCHA = True

	def test_panel_access_for_new_user(self):
		self.client.login(username='mamad', password='yY3Kky4Rz1S31v')

		response = self.client.get(reverse('wagtailadmin_home'))
		self.assertEqual(response.status_code, 200)

	def test_panel__login_redirect_for_non_authenticated_user(self):
		response = self.client.get(reverse('wagtailadmin_home'))
		self.assertEqual(response.status_code, 302)


class BlogPostTest(WagtailPageTests):
	@classmethod
	def setUpTestData(cls):
		WagtailPageTests.setUpTestData()

		BlogListingPage.get_root_nodes().first().add_child(instance=BlogListingPage(title='خانه'))

	def test_creating_under_homepage(self):
		self.assertCanCreateAt(BlogListingPage, BlogDetailPage)

	def test_creating_post(self):
		homepage = BlogListingPage.objects.get(title='خانه')
		self.assertCanCreate(homepage, BlogDetailPage, nested_form_data({
			'title': 'یک پست آزمایشی فوق‌العاده',
			'intro': 'یک پرنده‌ی آرزو دار',
			'slug': 'great-post',
			'body': streamfield([
				('heading', 'تست کردن کار شایسته‌ای است'),
				('text', 'یونیت‌تست می‌نویسیم تا بدانیم وب‌سایتمان درست کار می‌کند'),
			])
		}))

from django.test import TestCase
from django.urls import reverse

from blog.models import BlogListingPage, BlogDetailPage
from accounts.models import User

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

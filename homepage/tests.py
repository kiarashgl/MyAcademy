from django.test import SimpleTestCase
from django.urls import reverse

class HomePageTest(SimpleTestCase):
	def test_homepage_template(self):
		response = self.client.get(reverse('home'))

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'index.html')
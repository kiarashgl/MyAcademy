from django.test import TestCase
from django.urls import reverse

from accounts.models import User

class LoginTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		User.objects.create_user(username='mamad', password='NAZEomae')

	def test_login_template(self):
		response = self.client.get(reverse('accounts:login'))

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'registration/login.html')

	def test_login_successful(self):
		login = self.client.login(username='mamad', password='NAZEomae')

		self.assertTrue(login)

	def test_login_successful_redirect(self):
		response = self.client.post(reverse('accounts:login'), {'username':'mamad', 'password':'NAZEomae'})

		self.assertRedirects(response, reverse('home'))
		self.assertIn('_auth_user_id', self.client.session)

	def test_login_wrong_password(self):
		response = self.client.post(reverse('accounts:login'), {'username':'mamad', 'password':'SoWrong132'})

		self.assertEqual(response.status_code, 200)
		self.assertNotIn('_auth_user_id', self.client.session)

	def test_login_wrong_username(self):
		response = self.client.post(reverse('accounts:login'), {'username':'wrong_desu', 'password':'SoWrong132'})

		self.assertEqual(response.status_code, 200)
		self.assertNotIn('_auth_user_id', self.client.session)

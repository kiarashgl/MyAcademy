import shutil

from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse

import tempfile
from accounts.models import User

MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class ProfileTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		User.objects.create_user(username='user1',
		                         first_name='fname',
		                         last_name='lname',
		                         email='my_mail@example.com',
		                         password='SomeRandomStuff',
		                         university='Sharif',
		                         major='CE',
		                         bio='People are awesome')

	@classmethod
	def tearDownClass(cls):
		shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
		super().tearDownClass()

	def setUp(self):
		self.user = User.objects.get(username='user1')
		self.client.login(
			username='user1', password='SomeRandomStuff'
		)

	def test_profile_template(self):
		response = self.client.get(reverse('accounts:profile'))

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'registration/profile.html')

	def test_profile_redirect(self):
		self.client.logout()
		response = self.client.get(reverse('accounts:profile'))

		# Redirect to home if user is not logged in
		self.assertEqual(response.url, reverse('accounts:login') + '?next=/accounts/profile/')


	def test_profile_successful(self):
		response = self.client.get(reverse('accounts:profile'))

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'registration/profile.html')

		self.assertContains(response, self.user.first_name)
		self.assertContains(response, self.user.last_name)
		self.assertContains(response, self.user.university)
		self.assertContains(response, self.user.major)
		self.assertContains(response, self.user.bio)
		self.assertContains(response, self.user.profile_picture)

	def test_profile_change_texts(self):
		new_first_name = 'OOOOLaLa'
		new_last_name = 'OOOOadsadgsddgsfLaLa'
		new_university = 'fggfafadsfsdf'
		new_major = '98tt5g683sd53sdf5sdf'

		data = {'first_name': new_first_name,
		        'last_name': new_last_name,
		        'university': new_university,
		        'major': new_major,
		        'profile_picture': ''}
		response = self.client.post(reverse('accounts:profile_edit'), data)

		self.assertEqual(response.status_code, 302)

		self.user.refresh_from_db()
		self.assertEqual(self.user.first_name, new_first_name)
		self.assertEqual(self.user.last_name, new_last_name)
		self.assertEqual(self.user.university, new_university)
		self.assertEqual(self.user.major, new_major)

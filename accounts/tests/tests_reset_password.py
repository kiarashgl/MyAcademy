from django.test import TestCase
from django.urls import reverse
from django.core import mail

from accounts.models import User


class ResetPasswordTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		User.objects.create_user(username='uzumaki_naruto', email='naruto@konoha.ho', password='IL0V3RamEn')

	def test_password_reset_template(self):
		self.assertTrue(self.client.login(username='uzumaki_naruto', password='IL0V3RamEn'))

		response = self.client.get(reverse('accounts:password_reset'))

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'registration/password_reset_form.html')

	def test_normal_password_request_email(self):
		response = self.client.post(reverse('accounts:password_reset'),
									{'email': 'naruto@konoha.ho'})

		# Check the email is sent and you are redirected to done
		self.assertRedirects(response, reverse('accounts:password_reset_done'))
		self.assertTemplateUsed(response, 'registration/password_reset_subject.txt')
		self.assertTemplateUsed(response, 'registration/password_reset_email.html')
		self.assertEqual(len(mail.outbox), 1)

		# Check you can access the reset link
		uid, token = response.context['uid'], response.context['token']
		response = self.client.get(reverse('accounts:password_reset_confirm',
										   kwargs={'uidb64': uid, 'token': token}))
		self.assertRedirects(response, f'/accounts/reset/{uid}/set-password/')

		# Check it resets the password and redirects you to login
		response = self.client.post(response.url, {'new_password1': 'SASUKEwaTOMODACHIda',
												   'new_password2': 'SASUKEwaTOMODACHIda'})
		self.assertRedirects(response, reverse('accounts:login'))

		# Check the password is actually reset
		self.assertTrue(self.client.login(username='uzumaki_naruto', password='SASUKEwaTOMODACHIda'))

	def test_wrong_password_reset_email(self):
		response = self.client.post(reverse('accounts:password_reset'), {'email': 'nosuch@email.org'})

		self.assertRedirects(response, reverse('accounts:password_reset_done'))
		self.assertEqual(len(mail.outbox), 0)

	def test_reset_email_expires(self):
		response = self.client.post(reverse('accounts:password_reset'),
									{'email': 'naruto@konoha.ho'})

		uid, token = response.context['uid'], response.context['token']
		response = self.client.get(reverse('accounts:password_reset_confirm',
										   kwargs={'uidb64': uid, 'token': token}))

		# Reset email once
		response = self.client.post(response.url, {'new_password1': 'SASUKEwaTOMODACHIda',
												   'new_password2': 'SASUKEwaTOMODACHIda'})

		response = self.client.get(reverse('accounts:password_reset_confirm',
										   kwargs={'uidb64': uid, 'token': token}))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.context['messages']), 1)

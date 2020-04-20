from django.test import TestCase
from django.urls import reverse

from accounts.models import User

class SignUpTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		User.objects.create_user(username='mamad', first_name='ممد', last_name='ممدی',
		 email='mamad@mamadi.ir', password='yY3Kky4Rz1S31v')

	def test_signup_template(self):
		response = self.client.get(reverse('accounts:signup'))

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'registration/signup.html')

	def test_signupـsuccessful(self):
		response = self.client.post(reverse('accounts:signup'), {'username': 'aliZ', 'first_name': 'Ali', 
			'last_name': 'Alavi', 'email': 'ali@alavi.ir', 
			'password1': 'yY3Kky4Rz1S31v', 'password2': 'yY3Kky4Rz1S31v'})

		# Check the user is redirected to the login page
		self.assertRedirects(response, reverse('accounts:login'))
		user = User.objects.get(username='aliZ')

		# Check the user information is correct
		self.assertEqual(user.first_name, 'Ali')
		self.assertEqual(user.last_name, 'Alavi')
		self.assertEqual(user.email, 'ali@alavi.ir')

	def test_signup_missing_required_field(self):
		response = self.client.post(reverse('accounts:signup'), {})

		self.assertEqual(response.status_code, 200)

		self.assertFormError(response, 'form', 'username', 'این فیلد لازم است.')
		self.assertFormError(response, 'form', 'first_name', 'این فیلد لازم است.')
		self.assertFormError(response, 'form', 'last_name', 'این فیلد لازم است.')
		self.assertFormError(response, 'form', 'email', 'این فیلد لازم است.')
		self.assertFormError(response, 'form', 'password1', 'این فیلد لازم است.')
		self.assertFormError(response, 'form', 'password2', 'این فیلد لازم است.')

		with self.assertRaises(User.DoesNotExist):
			User.objects.get(username='')

	def test_signup_existing_username(self):
		response = self.client.post(reverse('accounts:signup'), {'username':'mamad', 'first_name':'hoho',
			'last_name':'jotaro', 'email':'jiovanna', 'password1': 'yY3Kky4Rz1S31v', 'password2': 'yY3Kky4Rz1S31v'})

		self.assertEqual(response.status_code, 200)
		self.assertFormError(response, 'form', 'username', 'کاربری با آن نام کاربری وجود دارد.')

	def test_signup_password_mismatch(self):
		response = self.client.post(reverse('accounts:signup'), {'username':'dio', 'first_name':'hoho',
			'last_name':'jotaro', 'email':'jiovanna@giorno.ir', 
			'password1': 'yY3Kky4Rz1S31v', 'password2': 'XYZKky4Rz1S31v'})

		self.assertEqual(response.status_code, 200)

		self.assertFormError(response, 'form', 'password2', 'The two password fields didn’t match.')

		with self.assertRaises(User.DoesNotExist):
			User.objects.get(username='dio')

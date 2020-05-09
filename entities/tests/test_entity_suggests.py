import shutil

from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse

import tempfile
from accounts.models import User
from entities.models import Professor, University, Department

MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class SuggestTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		user = User.objects.create_user(username='user1',
										first_name='fname',
										last_name='lname',
										email='my_mail@example.com',
										password='SomeRandomStuff',
										university='Sharif',
										major='CE',
										bio='People are awesome')

		user.is_staff = True
		user.is_superuser = True
		user.is_active = True
		user.save()

		university_verified = University.objects.create(verified=True,
														name='Uni1',
														address='Blah blah, blah, blah')

		department_verified = Department.objects.create(verified=True,
														name='Dep1',
														my_university=university_verified)

		professor_verified = Professor.objects.create(verified=True,
													  first_name='robert',
													  last_name='jones',
													  my_department=department_verified)

	@classmethod
	def tearDownClass(cls):
		shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
		super().tearDownClass()

	def setUp(self):
		self.user = User.objects.get(username='user1')
		self.client.login(
			username='user1', password='SomeRandomStuff'
		)

		self.professor = Professor.objects.get(pk=1)
		self.department = Department.objects.get(pk=1)
		self.university = University.objects.get(pk=1)

	def test_suggest_valid_professor(self):
		response = self.client.post(reverse('entities:professor_suggest'),
									{'first_name': 'محمد علی',
									 'last_name': 'آبام',
									 'my_department': self.department.pk})

		# Check the user is redirected to the home page
		self.assertRedirects(response, reverse('home'))

		# Check the user information is correct
		prof = Professor.objects.get(first_name='محمد علی', last_name='آبام')
		self.assertEqual(prof.first_name, 'محمد علی')
		self.assertEqual(prof.last_name, 'آبام')
		self.assertEqual(prof.my_department, self.department)
		self.assertEqual(prof.verified, False)

	def test_suggest_invalid_professor(self):
		response = self.client.post(reverse('entities:professor_suggest'),
									{'first_name': self.professor.first_name,
									 'last_name': self.professor.last_name,
									 'my_department': self.department.pk})

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'وجود دارد.')

	def test_suggest_verify_unverify_professor(self):
		for i in range(10):
			url = reverse('entities:professor_suggest')
			data = {'first_name': 'Mohammad ' + str(i),
					'last_name': 'Abam',
					'my_department': self.department.pk}
			self.client.post(url, data)

		to_be_verified = Professor.objects.filter(first_name__istartswith='Mohammad ').values_list('pk', flat=True)

		for prof in list(Professor.objects.filter(first_name__istartswith='Mohammad ')):
			self.assertEqual(prof.verified, False)

		verify_url = '/admin/entities/professor/'
		data = {
			'action': 'make_verified',
			'_selected_action': to_be_verified
		}
		self.client.post(verify_url, data, follow=True)

		for prof in list(Professor.objects.filter(first_name__istartswith='Mohammad ')):
			self.assertEqual(prof.verified, True)

		verify_url = '/admin/entities/professor/'
		data = {
			'action': 'make_unverified',
			'_selected_action': to_be_verified
		}
		self.client.post(verify_url, data, follow=True)

		for prof in list(Professor.objects.filter(first_name__istartswith='Mohammad ')):
			self.assertEqual(prof.verified, False)

	def test_suggest_valid_department(self):
		response = self.client.post(reverse('entities:department_suggest'),
									{'name': 'دانشکده شیمی',
									 'my_university': self.university.pk})

		# Check the user is redirected to the home page
		self.assertRedirects(response, reverse('home'))

		# Check the user information is correct
		dep = Department.objects.get(name='دانشکده شیمی')
		self.assertEqual(dep.name, 'دانشکده شیمی')
		self.assertEqual(dep.my_university, self.university)
		self.assertEqual(dep.verified, False)

	def test_suggest_invalid_department(self):
		response = self.client.post(reverse('entities:department_suggest'),
									{'name': self.department.name,
									 'my_university': self.department.my_university.pk})

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'وجود دارد.')

	def test_suggest_verify_unverify_department(self):
		for i in range(10):
			url = reverse('entities:department_suggest')
			data = {'name': 'Dep ' + str(i) + " end",
					'my_university': self.university.pk}
			self.client.post(url, data)

		to_be_verified = Department.objects.filter(name__istartswith='Dep ').values_list('pk', flat=True)

		for dep in list(Department.objects.filter(name__istartswith='Dep ')):
			self.assertEqual(dep.verified, False)

		verify_url = '/admin/entities/department/'
		data = {
			'action': 'make_verified',
			'_selected_action': to_be_verified
		}
		self.client.post(verify_url, data, follow=True)

		for dep in list(Department.objects.filter(name__istartswith='Dep ')):
			self.assertEqual(dep.verified, True)

		verify_url = '/admin/entities/department/'
		data = {
			'action': 'make_unverified',
			'_selected_action': to_be_verified
		}
		self.client.post(verify_url, data, follow=True)

		for dep in list(Department.objects.filter(name__istartswith='Dep ')):
			self.assertEqual(dep.verified, False)

	def test_suggest_valid_university(self):
		response = self.client.post(reverse('entities:university_suggest'),
									{'name': 'دانشگاه علم و صنعت',
									 'address': 'خیابان ستارخان، نرسیده به پمپ بنزین'})

		# Check the user is redirected to the home page
		self.assertRedirects(response, reverse('home'))

		# Check the user information is correct
		uni = University.objects.get(name='دانشگاه علم و صنعت')
		self.assertEqual(uni.name, 'دانشگاه علم و صنعت')
		self.assertEqual(uni.address, 'خیابان ستارخان، نرسیده به پمپ بنزین')
		self.assertEqual(uni.verified, False)

	def test_suggest_invalid_university(self):
		response = self.client.post(reverse('entities:university_suggest'),
									{'name': self.university.name,
									 'address': self.university.address})

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'موجود است.')

	def test_suggest_verify_unverify_university(self):
		for i in range(10):
			url = reverse('entities:university_suggest')
			data = {'name': 'Uni ' + str(i) + " end",
					'address': 'Some random string'}
			self.client.post(url, data)

		to_be_verified = University.objects.filter(name__istartswith='Uni ').values_list('pk', flat=True)

		for uni in list(University.objects.filter(name__istartswith='Uni ')):
			self.assertEqual(uni.verified, False)

		verify_url = '/admin/entities/university/'
		data = {
			'action': 'make_verified',
			'_selected_action': to_be_verified
		}
		self.client.post(verify_url, data, follow=True)

		for uni in list(University.objects.filter(name__istartswith='Uni ')):
			self.assertEqual(uni.verified, True)

		verify_url = '/admin/entities/university/'
		data = {
			'action': 'make_unverified',
			'_selected_action': to_be_verified
		}
		self.client.post(verify_url, data, follow=True)

		for uni in list(University.objects.filter(name__istartswith='Uni ')):
			self.assertEqual(uni.verified, False)

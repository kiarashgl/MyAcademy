import shutil

from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse

import tempfile
from accounts.models import User
from entities.models import Professor, University, Department

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

		university_verified = University.objects.create(verified=True,
														name='Uni1',
														address='Blah blah, blah, blah')

		university_unverified = University.objects.create(verified=False,
														  name='Uni2',
														  address='Blah blah, blah, blah')

		for i in range(10):
			University.objects.create(verified=(i % 2 == 0),
									  name='Uni ' + str(i) + " end",
									  address='No address yet')

		department_verified = Department.objects.create(verified=True,
														name='Dep1',
														my_university=university_verified)

		department_unverified = Department.objects.create(verified=False,
														  name='Dep2 unverified',
														  my_university=university_verified)

		for i in range(20):
			Department.objects.create(verified=(i % 2 == 0),
									  name='Dep unverified' + str(i) + " end",
									  my_university=university_verified)

		professor_verified = Professor.objects.create(verified=True,
													  first_name='robert',
													  last_name='jones',
													  my_department=department_verified)

		professor_unverified = Professor.objects.create(verified=False,
														first_name='robert unverified',
														last_name='jones unverified',
														my_department=department_verified)

		for i in range(50):
			Professor.objects.create(verified=(i % 2 == 0),
									 first_name='first name ' + str(i),
									 last_name='last name ' + str(i) + " end",
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

	def test_verified_professor_profile(self):
		response = self.client.get(reverse('entities:professor_detail', kwargs={'pk': 1}))

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'entities/professor_detail.html')

		self.assertContains(response, "مدرس")
		self.assertContains(response, self.professor.first_name)
		self.assertContains(response, self.professor.last_name)
		self.assertContains(response, self.professor.my_department)
		self.assertContains(response, self.professor.my_department.my_university)
		self.assertContains(response, self.professor.picture)

	def test_unverified_professor_profile(self):
		response = self.client.get(reverse('entities:professor_detail', kwargs={'pk': 2}))
		self.assertEqual(response.status_code, 404)

	def test_professor_all_page(self):
		response = self.client.get(reverse('entities:professor_all'))

		self.assertEqual(response.status_code, 200)

		for prof in list(Professor.objects.filter(verified=True)):
			self.assertContains(response, prof)
			self.assertContains(response, prof.my_department)

		for prof in list(Professor.objects.filter(verified=False)):
			self.assertNotContains(response, prof)

		self.assertContains(response, "entity-card", count=len(list(Professor.objects.filter(verified=True))))

	def test_verified_department_profile(self):
		response = self.client.get(reverse('entities:department_detail', kwargs={'pk': 1}))

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'entities/department_detail.html')

		self.assertContains(response, "دانشکده")
		self.assertContains(response, self.department.name)
		self.assertContains(response, self.department.my_university)
		self.assertContains(response, self.department.picture)

	def test_unverified_department_profile(self):
		response = self.client.get(reverse('entities:department_detail', kwargs={'pk': 2}))
		self.assertEqual(response.status_code, 404)

	def test_department_all_page(self):
		response = self.client.get(reverse('entities:department_all'))

		self.assertEqual(response.status_code, 200)

		for dep in list(Department.objects.filter(verified=True)):
			self.assertContains(response, dep)
			self.assertContains(response, dep.my_university)

		for dep in list(Department.objects.filter(verified=False)):
			self.assertNotContains(response, dep)

		self.assertContains(response, "entity-card", count=len(list(Department.objects.filter(verified=True))))

	def test_verified_university_profile(self):
		response = self.client.get(reverse('entities:university_detail', kwargs={'pk': 1}))

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'entities/university_detail.html')

		self.assertContains(response, "دانشگاه")
		self.assertContains(response, self.university.name)
		self.assertContains(response, self.university.picture)

	def test_unverified_university_profile(self):
		response = self.client.get(reverse('entities:university_detail', kwargs={'pk': 2}))
		self.assertEqual(response.status_code, 404)

	def test_university_all_page(self):
		response = self.client.get(reverse('entities:university_all'))

		self.assertEqual(response.status_code, 200)

		for uni in list(University.objects.filter(verified=True)):
			self.assertContains(response, uni)

		for uni in list(University.objects.filter(verified=False)):
			self.assertNotContains(response, uni)

		self.assertContains(response, "entity-card", count=len(list(University.objects.filter(verified=True))))

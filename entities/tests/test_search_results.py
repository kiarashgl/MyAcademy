import shutil

from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.db.models import Q
import random

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

		universities = []
		departments = []

		for _ in range(30):
			uni_name = get_random_string(length=10)
			uni_address = get_random_string(length=20)
			universities.append(
				University.objects.create(verified=bool(random.getrandbits(1)), name=uni_name, address=uni_address))

		for _ in range(40):
			dep_name = get_random_string(length=10)
			uni = universities[random.randint(0, len(universities) - 1)]
			departments.append(
				Department.objects.create(verified=bool(random.getrandbits(1)), name=dep_name, my_university=uni))

		for _ in range(50):
			prof_first_name = get_random_string(length=20)
			prof_last_name = get_random_string(length=20)
			dep = departments[random.randint(0, len(departments) - 1)]
			Professor.objects.create(
				verified=bool(random.getrandbits(1)), first_name=prof_first_name, last_name=prof_last_name,
				my_department=dep)

	@classmethod
	def tearDownClass(cls):
		shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
		super().tearDownClass()

	def setUp(self):
		self.user = User.objects.get(username='user1')
		self.client.login(
			username='user1', password='SomeRandomStuff'
		)

	def test_search_length(self):
		import string

		for char in list(string.ascii_lowercase):
			profs = list(
				Professor.objects.filter(Q(first_name__icontains=char) | Q(last_name__icontains=char), verified=True))
			deps = list(Department.objects.filter(name__icontains=char, verified=True))
			unis = list(University.objects.filter(name__icontains=char, verified=True))

			counts = len(profs) + len(deps) + len(unis)

			data = {'q': char}

			response = self.client.get(reverse('entities:search_results'), data)

			self.assertContains(response, 'entity-card', count=counts)

	def test_search_filtered_by_all(self):
		import string

		for char in list(string.ascii_lowercase):
			profs = list(
				Professor.objects.filter(Q(first_name__icontains=char) | Q(last_name__icontains=char), verified=True))
			deps = list(Department.objects.filter(name__icontains=char, verified=True))
			unis = list(University.objects.filter(name__icontains=char, verified=True))

			counts = len(profs) + len(deps) + len(unis)

			data = {'q': char, 'filter_by': 'all'}

			response = self.client.get(reverse('entities:search_results'), data)

			self.assertContains(response, 'entity-card', count=counts)

			for prof in profs:
				self.assertContains(response, prof.first_name)
				self.assertContains(response, prof.last_name)
				self.assertContains(response, prof.my_department)

			for dep in deps:
				self.assertContains(response, dep.name)
				self.assertContains(response, dep.my_university)

			for uni in unis:
				self.assertContains(response, uni.name)

	def test_search_filtered_by_profs(self):
		import string

		for char in list(string.ascii_lowercase):
			profs = list(
				Professor.objects.filter(Q(first_name__icontains=char) | Q(last_name__icontains=char), verified=True))

			counts = len(profs)

			data = {'q': char, 'filter_by': 'profs'}

			response = self.client.get(reverse('entities:search_results'), data)

			self.assertContains(response, 'entity-card', count=counts)

			for prof in profs:
				self.assertContains(response, prof.first_name)
				self.assertContains(response, prof.last_name)
				self.assertContains(response, prof.my_department)

	def test_search_filtered_by_deps(self):
		import string

		for char in list(string.ascii_lowercase):
			deps = list(Department.objects.filter(name__icontains=char, verified=True))

			counts = len(deps)

			data = {'q': char, 'filter_by': 'deps'}

			response = self.client.get(reverse('entities:search_results'), data)

			self.assertContains(response, 'entity-card', count=counts)

			for dep in deps:
				self.assertContains(response, dep.name)
				self.assertContains(response, dep.my_university)

	def test_search_filtered_by_unis(self):
		import string

		for char in list(string.ascii_lowercase):
			unis = list(University.objects.filter(name__icontains=char, verified=True))

			counts = len(unis)

			data = {'q': char, 'filter_by': 'unis'}

			response = self.client.get(reverse('entities:search_results'), data)

			self.assertContains(response, 'entity-card', count=counts)

			for uni in unis:
				self.assertContains(response, uni.name)

from django.test import LiveServerTestCase

from MyAcademy.settings import SELENIUM_ON_LINUX, SKIP_SELENIUM_TESTS
from accounts.models import User

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import shutil

from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.db.models import Q
import random
from unittest import skipIf

import tempfile
from accounts.models import User
from entities.models import Professor, University, Department

MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class End2EndTestCase(LiveServerTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		if not SKIP_SELENIUM_TESTS:
			if SELENIUM_ON_LINUX:
				options = webdriver.ChromeOptions()
				options.add_argument("--headless")
				cls.selenium = webdriver.Chrome(options=options, executable_path='webdriver/chromedriver')
			else:
				cls.selenium = webdriver.Firefox(executable_path='webdriver/geckodriver.exe')
			cls.selenium.implicitly_wait(10)

	@classmethod
	def tearDownClass(cls):
		shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
		if not SKIP_SELENIUM_TESTS:
			cls.selenium.quit()
		super().tearDownClass()

	@skipIf(SKIP_SELENIUM_TESTS, "Don't want to test")
	def test_end2end(self):
		# Create a new user and login
		self.selenium.get('%s%s' % (self.live_server_url, reverse('home')))
		self.selenium.find_element(By.LINK_TEXT, "ثبت‌نام").click()
		self.selenium.find_element(By.ID, "id_username").click()
		self.selenium.find_element(By.ID, "id_username").send_keys("user2")
		self.selenium.find_element(By.ID, "id_first_name").send_keys("اسم")
		self.selenium.find_element(By.ID, "id_last_name").send_keys("فامیل")
		self.selenium.find_element(By.ID, "id_email").send_keys("addr@ex.com")
		self.selenium.find_element(By.ID, "id_password1").send_keys("Ax123456789")
		self.selenium.find_element(By.ID, "id_password2").send_keys("Ax123456789")
		self.selenium.find_element(By.ID, "submit-id-submit").click()

		self.selenium.find_element(By.ID, "id_username").send_keys("user2")
		self.selenium.find_element(By.ID, "id_password").send_keys("Ax123456789")
		self.selenium.find_element(By.CSS_SELECTOR, ".bg-light-purple:nth-child(4)").click()

		user = User.objects.get(username="user2")
		user.is_superuser = True
		user.is_staff = True
		user.is_active = True
		user.save()

		universities = []
		departments = []
		for _ in range(5):
			uni_name = "Uni " + str(get_random_string(length=10))
			uni_address = get_random_string(length=20)

			universities.append(uni_name)

			self.selenium.get('%s%s' % (self.live_server_url, reverse('entities:university_suggest')))
			self.selenium.find_element(By.ID, "id_name").send_keys(uni_name)
			self.selenium.find_element(By.ID, "id_address").send_keys(uni_address)
			self.selenium.find_element(By.ID, "submit-id-submit").click()

		self.selenium.get('%s%s' % (self.live_server_url, '/admin/entities/university/'))
		for elem in self.selenium.find_elements(By.CLASS_NAME, "action-select"):
			elem.click()
		self.selenium.find_element(By.NAME, "action").click()
		dropdown = self.selenium.find_element(By.NAME, "action")
		dropdown.find_element(By.XPATH, "//option[. = 'تایید موارد انتخاب شده']").click()
		self.selenium.find_element(By.NAME, "action").click()
		self.selenium.find_element(By.NAME, "index").click()

		for _ in range(5):
			dep_name = "Dep " + str(get_random_string(length=10))
			uni = str(University.objects.get(name=universities[random.randint(0, len(universities) - 1)]))

			departments.append(dep_name)

			self.selenium.get('%s%s' % (self.live_server_url, reverse('entities:department_suggest')))
			self.selenium.find_element(By.ID, "id_name").click()
			self.selenium.find_element(By.ID, "id_name").send_keys(dep_name)
			self.selenium.find_element(By.ID, "id_my_university").click()
			dropdown = self.selenium.find_element(By.ID, "id_my_university")
			dropdown.find_element(By.XPATH, "//option[. = '%s']" % uni).click()
			self.selenium.find_element(By.ID, "id_my_university").click()
			self.selenium.find_element(By.ID, "submit-id-submit").click()

		self.selenium.get('%s%s' % (self.live_server_url, '/admin/entities/department/'))
		for elem in self.selenium.find_elements(By.CLASS_NAME, "action-select"):
			elem.click()
		self.selenium.find_element(By.NAME, "action").click()
		dropdown = self.selenium.find_element(By.NAME, "action")
		dropdown.find_element(By.XPATH, "//option[. = 'تایید موارد انتخاب شده']").click()
		self.selenium.find_element(By.NAME, "action").click()
		self.selenium.find_element(By.NAME, "index").click()

		for _ in range(5):
			prof_first_name = "Prof " + str(get_random_string(length=20))
			prof_last_name = get_random_string(length=20)
			dep = Department.objects.get(name=departments[random.randint(0, len(departments) - 1)])
			dep_str = '%s - %s' % (dep, dep.my_university)

			self.selenium.get('%s%s' % (self.live_server_url, reverse('entities:professor_suggest')))
			self.selenium.find_element(By.ID, "id_first_name").send_keys(prof_first_name)
			self.selenium.find_element(By.ID, "id_last_name").click()
			self.selenium.find_element(By.ID, "id_last_name").send_keys(prof_last_name)
			self.selenium.find_element(By.ID, "id_my_department").click()
			dropdown = self.selenium.find_element(By.ID, "id_my_department")
			dropdown.find_element(By.XPATH, "//option[. = '%s']" % dep_str).click()
			self.selenium.find_element(By.ID, "id_my_department").click()
			self.selenium.find_element(By.ID, "submit-id-submit").click()

		self.selenium.get('%s%s' % (self.live_server_url, '/admin/entities/professor/'))
		for elem in self.selenium.find_elements(By.CLASS_NAME, "action-select"):
			elem.click()
		self.selenium.find_element(By.NAME, "action").click()
		dropdown = self.selenium.find_element(By.NAME, "action")
		dropdown.find_element(By.XPATH, "//option[. = 'تایید موارد انتخاب شده']").click()
		self.selenium.find_element(By.NAME, "action").click()
		self.selenium.find_element(By.NAME, "index").click()

		self.selenium.get('%s%s' % (self.live_server_url, reverse('home')))
		self.selenium.find_element(By.LINK_TEXT, "دانشگاه‌ها").click()

		self.selenium.get('%s%s' % (self.live_server_url, reverse('home')))
		self.selenium.find_element(By.LINK_TEXT, "دانشکده‌ها").click()

		self.selenium.get('%s%s' % (self.live_server_url, reverse('home')))
		self.selenium.find_element(By.LINK_TEXT, "اساتید").click()

from django.test import LiveServerTestCase
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
from unittest import skip

import tempfile
from accounts.models import User
from entities.models import Professor, University, Department

MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class End2EndTestCase(LiveServerTestCase):

	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		cls.selenium = webdriver.Firefox(executable_path='webdriver/geckodriver.exe')
		cls.selenium.implicitly_wait(10)

	@classmethod
	def tearDownClass(cls):
		shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
		cls.selenium.quit()
		super().tearDownClass()

	@skip("Don't want to test")
	def test_create_user(self):
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

	@skip("Don't want to test")
	def test_change_profile(self):
		self.test_create_user()
		self.selenium.get('%s%s' % (self.live_server_url, reverse('home')))

		self.selenium.find_element(By.CSS_SELECTOR, ".rounded-circle").click()
		self.selenium.find_element(By.CSS_SELECTOR, ".dropdown-item:nth-child(2) > span").click()
		self.selenium.find_element(By.CSS_SELECTOR, ".fas").click()
		self.selenium.find_element(By.ID, "id_first_name").click()
		self.selenium.find_element(By.ID, "id_first_name").send_keys("اسمlllllll")
		self.selenium.find_element(By.ID, "id_university").send_keys("دانشگاه صنعتی شریف")
		self.selenium.find_element(By.ID, "id_major").send_keys("مهندسی کامپیوتر")
		self.selenium.find_element(By.ID, "id_bio").click()
		self.selenium.find_element(By.ID, "id_bio").send_keys("I love chickens.")
		self.selenium.find_element(By.ID, "submit-id-submit").click()
		self.selenium.find_element(By.CSS_SELECTOR, ".close > span").click()

from django.test import LiveServerTestCase

from MyAcademy.settings import SELENIUM_ON_LINUX, SKIP_SELENIUM_TESTS

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import shutil

from django.test.utils import override_settings
from django.urls import reverse_lazy

import tempfile
from accounts.models import User
from unittest import skipIf

MEDIA_ROOT = tempfile.mkdtemp()

from MyAcademy import settings


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

			settings.DISABLE_RECAPTCHA = True

	@classmethod
	def tearDownClass(cls):
		shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
		if not SKIP_SELENIUM_TESTS:
			cls.selenium.quit()
		super().tearDownClass()

	def setUp(self):
		user = User.objects.create_superuser(username='admin',
											 email='my_mail@example.com',
											 password='admin')
		user.save()

	@skipIf(SKIP_SELENIUM_TESTS, "Don't want to test")
	def test_create_blog(self):
		self.selenium.get('%s%s' % (self.live_server_url, '/cms-admin/'))

		# Log in
		self.selenium.find_element(By.ID, "id_username").send_keys("admin")
		self.selenium.find_element(By.ID, "id_password").send_keys("admin")
		self.selenium.find_element(By.ID, "id_password").send_keys(Keys.ENTER)

		# Change language settings to english
		self.selenium.find_element(By.CSS_SELECTOR, ".icon-arrow-up-after").click()
		self.selenium.find_element(By.LINK_TEXT, "تنظیمات حساب").click()
		self.selenium.find_element(By.CSS_SELECTOR, ".row:nth-child(5) .button").click()
		self.selenium.find_element(By.ID, "id_preferred_language").click()
		dropdown = self.selenium.find_element(By.ID, "id_preferred_language")
		dropdown.find_element(By.XPATH, "//option[. = 'انگلیسی']").click()
		self.selenium.find_element(By.CSS_SELECTOR, ".button:nth-child(1)").click()

		# Change slug of "Welcome to your first ..." page to something other than home
		self.selenium.get('%s%s' % (self.live_server_url, '/cms-admin/'))
		self.selenium.find_element(By.LINK_TEXT, "Pages").click()
		self.selenium.find_element(By.LINK_TEXT, "Edit").click()
		self.selenium.find_element(By.ID, "id_slug").send_keys("not_home")
		self.selenium.find_element(By.NAME, "action-publish").click()

		# Create homepage
		self.selenium.get('%s%s' % (self.live_server_url, '/cms-admin/'))
		self.selenium.find_element(By.LINK_TEXT, "Pages").click()
		self.selenium.find_element(By.LINK_TEXT, "Explore").click()
		self.selenium.find_element(By.LINK_TEXT, "Add child page").click()
		self.selenium.find_element(By.LINK_TEXT, "Blog listing page").click()
		self.selenium.find_element(By.ID, "id_title").send_keys("Home page")
		self.selenium.find_element(By.ID, "id_slug").send_keys("home")
		self.selenium.find_element(By.NAME, "action-publish").click()

		# Create blog page
		self.selenium.find_elements(By.LINK_TEXT, "Add child page")[-1].click()
		self.selenium.find_element(By.LINK_TEXT, "Blog detail page").click()
		self.selenium.find_element(By.ID, "id_title").send_keys("Test blog")
		self.selenium.find_element(By.ID, "id_intro").send_keys("Test intro")
		self.selenium.find_element(By.ID, "id_slug").send_keys("test_blog")
		self.selenium.find_element(By.NAME, "action-publish").click()

		# View the blog live and test liking/disliking functionality
		self.selenium.get('%s%s' % (self.live_server_url, '/blog/home/test_blog/'))
		self.assertEqual(self.selenium.find_element(By.ID, "like").text, "0")
		self.assertEqual(self.selenium.find_element(By.ID, "dislike").text, "0")

		self.selenium.find_element(By.CLASS_NAME, "like-btn").click()
		self.assertEqual(self.selenium.find_element(By.ID, "like").text, "1")
		self.assertEqual(self.selenium.find_element(By.ID, "dislike").text, "0")

		self.selenium.find_element(By.CLASS_NAME, "like-btn").click()
		self.assertEqual(self.selenium.find_element(By.ID, "like").text, "0")
		self.assertEqual(self.selenium.find_element(By.ID, "dislike").text, "0")

		self.selenium.find_element(By.CLASS_NAME, "like-btn").click()
		self.assertEqual(self.selenium.find_element(By.ID, "like").text, "1")
		self.assertEqual(self.selenium.find_element(By.ID, "dislike").text, "0")

		self.selenium.find_element(By.CLASS_NAME, "dislike-btn").click()
		self.assertEqual(self.selenium.find_element(By.ID, "like").text, "0")
		self.assertEqual(self.selenium.find_element(By.ID, "dislike").text, "1")

		self.selenium.find_element(By.CLASS_NAME, "dislike-btn").click()
		self.assertEqual(self.selenium.find_element(By.ID, "like").text, "0")
		self.assertEqual(self.selenium.find_element(By.ID, "dislike").text, "0")

		self.selenium.find_element(By.CLASS_NAME, "dislike-btn").click()
		self.assertEqual(self.selenium.find_element(By.ID, "like").text, "0")
		self.assertEqual(self.selenium.find_element(By.ID, "dislike").text, "1")

		self.selenium.find_element(By.CLASS_NAME, "like-btn").click()
		self.assertEqual(self.selenium.find_element(By.ID, "like").text, "1")
		self.assertEqual(self.selenium.find_element(By.ID, "dislike").text, "0")

		# Add second blog page
		self.selenium.get('%s%s' % (self.live_server_url, '/cms-admin/'))
		self.selenium.find_element(By.LINK_TEXT, "Pages").click()
		self.selenium.find_element(By.LINK_TEXT, "Explore").click()
		self.selenium.find_elements(By.LINK_TEXT, "Add child page")[-1].click()
		self.selenium.find_element(By.LINK_TEXT, "Blog detail page").click()
		self.selenium.find_element(By.ID, "id_title").send_keys("Test blog 2")
		self.selenium.find_element(By.ID, "id_intro").send_keys("Test intro 2")
		self.selenium.find_element(By.ID, "id_slug").send_keys("test_blog_2")
		self.selenium.find_element(By.NAME, "action-publish").click()

		# See homepage
		self.selenium.get('%s%s' % (self.live_server_url, '/blog/home/'))

		# Test orderings
		self.selenium.get('%s%s' % (self.live_server_url, '/blog/home/?orderby=date'))
		blog_names = [x.text for x in self.selenium.find_elements(By.CLASS_NAME, 'card-header')]
		self.assertEqual(blog_names[0], 'Test blog 2')
		self.assertEqual(blog_names[1], 'Test blog')

		self.selenium.get('%s%s' % (self.live_server_url, '/blog/home/?orderby=popular'))
		blog_names = [x.text for x in self.selenium.find_elements(By.CLASS_NAME, 'card-header')]
		self.assertEqual(blog_names[0], 'Test blog')
		self.assertEqual(blog_names[1], 'Test blog 2')


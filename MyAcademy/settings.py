"""
Django settings for MyAcademy project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'MyAcademy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
	'django_comments_xtd',
	'django_comments',

	'blog',
	'ratings',
	'accounts',
	'entities',
	'core',

	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.sites',
	'crispy_forms',
	'django_cleanup',
	'django_nose',
	'rest_framework',

	'wagtail.contrib.forms',
	'wagtail.contrib.redirects',
	"wagtail.contrib.routable_page",
	'wagtail.embeds',
	'wagtail.sites',
	'wagtail.users',
	'wagtail.snippets',
	'wagtail.documents',
	'wagtail.images',
	'wagtail.search',
	'wagtail.admin',
	'wagtail.core',

	'captcha',

	'modelcluster',
	'taggit',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'MyAcademy.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(BASE_DIR, 'templates')],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
				'django.template.context_processors.media',
			],
		},
	},
]

REST_FRAMEWORK = {
	# Use Django's standard `django.contrib.auth` permissions,
	# or allow read-only access for unauthenticated users.
	'DEFAULT_PERMISSION_CLASSES': [
		'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
	]
}

WSGI_APPLICATION = 'MyAcademy.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
}

#LOGIN_URL = 'accounts.login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
AUTH_USER_MODEL = 'accounts.User'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
	{
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	},
]

# Email service 

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')

# Media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'fa'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATICFILES_DIRS = [
	os.path.join(BASE_DIR, "staticfiles"),
]

LOCALE_PATHS = (
	os.path.join(BASE_DIR, "locale"),
)

# Django Crispy Forms Config
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Use nose to run all tests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
	'--with-coverage',
	'--traverse-namespace',
	'--cover-package=accounts, entities',  # Add packages here
]

SELENIUM_ON_LINUX = False  # Set to true if you want to run selenium tests on linux (Probably on server)
SKIP_SELENIUM_TESTS = True  # Set to true if you want to skip selenium tests

local_settings_path = os.path.join(os.path.dirname(__file__), 'local_settings.py')
if os.path.exists(local_settings_path):
	exec(open(local_settings_path, 'rb').read())

WAGTAIL_SITE_NAME = 'MyAcademy'
BLOG_PAGINATION_PER_PAGE = 2

COMMENTS_APP = 'django_comments_xtd'
COMMENTS_XTD_MAX_THREAD_LEVEL = 2
COMMENTS_XTD_CONFIRM_EMAIL = False

COMMENTS_XTD_APP_MODEL_OPTIONS = {
	'default': {
		'allow_flagging': True,
		'allow_feedback': True,
		'show_feedback': True,
		'who_can_post': 'users'
	},
}

# ReCaptcha v3
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']
DISABLE_RECAPTCHA = False

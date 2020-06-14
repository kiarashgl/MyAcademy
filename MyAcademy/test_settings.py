import os

settings_path = os.path.join(os.path.dirname(__file__), 'settings.py')
if os.path.exists(settings_path):
    exec(open(settings_path, 'rb').read())

DEBUG = False
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'travis_ci_db',
            'USER': 'travis',
            'PASSWORD': '',
            'HOST': '127.0.0.1',
        }
    }

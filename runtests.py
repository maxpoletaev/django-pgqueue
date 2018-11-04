import sys
import os
import django
from django.conf import settings
from django.core.management import call_command


opts = {
    'INSTALLED_APPS': ['pgqueue'],
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': '127.0.0.1',
            'PORT': '5432',
            'NAME': 'pgqueue',
            'USER': 'postgres',
            'PASSWORD': '',
        },
    },
}


if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    settings.configure(**opts)
    django.setup()

    call_command('test', 'pgqueue')

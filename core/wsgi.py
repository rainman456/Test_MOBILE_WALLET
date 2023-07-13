"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
#import environ

from django.core.wsgi import get_wsgi_application
#from .settings.base import BASE_DIR
#env = environ.Env(DEBUG=(bool, False))
#environ.Env.read_env(BASE_DIR / '.env')
#SETTING = env('SETTING_FILE')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'core.settings.{SETTING}')

application = get_wsgi_application()

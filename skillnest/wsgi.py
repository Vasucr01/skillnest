"""
WSGI config for skillnest project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillnest.settings')

# AUTOMATIC SETUP (Runs on Vercel startup)
# This will run migrations and create your admin account on the first visit
from django.core.management import execute_from_command_line
try:
    execute_from_command_line(['manage.py', 'migrate', '--noinput'])
    execute_from_command_line(['manage.py', 'create_admin'])
except Exception as e:
    print(f"Startup setup: {e}")

application = get_wsgi_application()
app = application
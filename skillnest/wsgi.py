"""
WSGI config for skillnest project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import django
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillnest.settings')

# Initialize Django
django.setup()

# AUTOMATIC SETUP (Runs on Vercel startup)
# This triggers migrations and admin creation when the server starts
try:
    print("Running migrations...")
    call_command('migrate', interactive=False)
    print("Running create_admin...")
    call_command('create_admin')
except Exception as e:
    print(f"Startup setup error: {e}")

application = get_wsgi_application()
app = application
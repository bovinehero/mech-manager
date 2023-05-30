"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
# imports occur at runtime, so fail linter
# pylint:disable=import-error
from django.core.wsgi import get_wsgi_application
# pylint:enable=import-error

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()

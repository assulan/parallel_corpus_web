"""
WSGI config for parallel_corpus_web project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "parallel_corpus_web.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

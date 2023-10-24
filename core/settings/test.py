from core.settings.base import *  # noqa

DEBUG = True

IS_TESTING = True

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
CELERY_ALWAYS_EAGER = True

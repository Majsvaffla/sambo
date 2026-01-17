import os

import dj_database_url
import sentry_sdk

from . import *  # noqa

SECRET_KEY = os.environ["SECRET_KEY"]

DEBUG = False

ALLOWED_HOSTS: list[str] = ["sambo.tordavid.xyz"]

if "DATABASE_URL" in os.environ:
    DATABASES = {"default": dj_database_url.config()}

MEDIA_URL = "/media/"
MEDIA_ROOT = "/sambo/media"

STATIC_ROOT = "/sambo/static"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

if "BUGSINK_DSN" in os.environ:
    sentry_sdk.init(
        dsn=os.environ["BUGSINK_DSN"],
        traces_sample_rate=0,  # Bugsink does not support traces.
    )

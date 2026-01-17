from . import *  # noqa
from . import PROJECT_ROOT

SECRET_KEY = "used-for-local-debugging-only"  # cspell:disable-line

DEBUG = True

ALLOWED_HOSTS: list[str] = ["*"]

MEDIA_URL = "/media/"
MEDIA_ROOT = PROJECT_ROOT / ".dev-media"

SERVE_DEV_MEDIA = True

EMAIL_BACKEND = "sambo.utils.email_debug_backend.EmailBackend"

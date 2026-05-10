from . import *  # noqa
from . import PROJECT_ROOT

SECRET_KEY = "used-for-local-debugging-only"  # cspell:disable-line

DEBUG = True

ALLOWED_HOSTS: list[str] = ["*"]

EMAIL_BACKEND = "sambo.utils.email_debug_backend.EmailBackend"

STATIC_ROOT = PROJECT_ROOT.parent / ".dev-static"

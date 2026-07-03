import importlib.resources
from pathlib import Path

import dj_database_url
import django_stubs_ext

django_stubs_ext.monkeypatch()


DATABASES = {
    "default": dj_database_url.config(default="postgres:///sambo"),
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# Type hints (and docs) says a Traversable object is returned from importlib.resources.files but
# an actual Path object is returned runtime thus we wrap it in its constructor to force the proper type.
# error: Argument 1 to "Path" has incompatible type "Traversable"; expected "str | PathLike[str]"
PROJECT_ROOT = Path(importlib.resources.files("sambo"))  # type: ignore[arg-type]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "sambo",
    "sambo.todo",
    "sambo.expense",
    "sambo.share",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "sambo.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(PROJECT_ROOT / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "sambo.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


LANGUAGE_CODE = "sv-se"

TIME_ZONE = "Europe/Stockholm"

USE_I18N = True

USE_L10N = True

USE_THOUSAND_SEPARATOR = True

STATIC_URL = "/static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATICFILES_DIRS = [
    PROJECT_ROOT / "static",
]
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

AUTH_USER_MODEL = "sambo.User"

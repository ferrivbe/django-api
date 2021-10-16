"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os

from decouple import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = config("SECRET_KEY", default="###SECRET_KEY###")

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = ["*"]

USE_X_FORWARDED_HOST = False
SESSION_COOKIE_HTTPONLY = True

SERVER_URL = os.getenv("SERVER_URL", default="*")


APPEND_SLASH = False

# Application definition

BACKEND_APPS = [
    "api",
    "drf_yasg",
]
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "rest_framework",
    "backend.utils",
] + BACKEND_APPS

MIDDLEWARE = [
    "backend.middleware.HealthCheckAwareSessionMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "backend.middleware.HeaderNoCacheMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB", default="postgres"),
        "USER": config("POSTGRES_USER", default="postgres"),
        "PASSWORD": config("POSTGRES_PASSWORD", default="postgres"),
        "HOST": config("POSTGRES_HOSTNAME", default="postgres"),
        "PORT": 5432,
        "CONN_MAX_AGE": 600,
        "DISABLE_SERVER_SIDE_CURSORS": True,
    },
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "../collected_static")

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "fluent_formatter": {
            "()": "backend.logging_formatter.VerboseFluentRecordFormatter",
            "format": {
                "level": "%(levelname)s",
                "pathname": "%(pathname)s",
                "hostname": "%(hostname)s",
                "logger": "%(name)s",
                "module": "%(module)s",
                "funcname": "%(funcName)s",
                "namespace": os.getenv("KUBERNETES_NAMESPACE", "localhost"),
                "release": os.getenv("GIT_HASH", "local"),
            },
            "encoder_class": "django.core.serializers.json.DjangoJSONEncoder",
            "raise_on_format_error": DEBUG,
        },
        "simple": {
            "format": "[{asctime}] {levelname} {message}",
            "style": "{",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        },
    },
    "filters": {"require_debug_true": {"()": "django.utils.log.RequireDebugTrue"}},
    "handlers": {
        "sentry": {
            "level": "WARNING",
            "class": "sentry_sdk.integrations.logging.EventHandler",
        },
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "filters": ["require_debug_true"],
        },
        "fluent": {
            "class": "fluent.handler.FluentHandler",
            "host": os.getenv("FLUENT_HOST", "fluentbit"),
            "port": int(os.getenv("FLUENT_PORT", 24224)),
            "tag": os.getenv("FLUENT_TAG", "catalog"),
            "formatter": "fluent_formatter",
            "level": "INFO",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
    },
    "root": {"level": "WARNING", "handlers": ["sentry"]},
    "loggers": {
        "django": {"handlers": ["console"], "propagate": True},
        "django.db": {
            "handlers": ["console"],
            "propagate": False,
            "level": os.getenv("DB_LOGGING_LEVEL", "INFO"),
        },
        "django.server": {"handlers": ["django.server"], "propagate": False},
        "server": {
            "handlers": ["fluent", "console"],
            "level": os.getenv("APP_LOGGING_LEVEL", "INFO"),
            "propagate": True,
        },
    },
}

SWAGGER_SETTINGS = {"USE_SESSION_AUTH": False}

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ]
}

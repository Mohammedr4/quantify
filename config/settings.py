"""
Django settings for the Quantify "pro" project.
This is the "bulletproof," "non-slop" settings file.
"""

import environ  # <--- This is "pro"
import os  # <--- This is "pro"
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- "Pro" django-environ Setup ---
env = environ.Env()  # <--- This is the "pro" instance
# We "outlaw" "slop" static methods. We use the "pro" instance:
env.read_env(os.path.join(BASE_DIR, ".env"))  # This reads your .env file

# --- "Pro" Security Keys ---
# We "outlaw" hardcoding "slop" keys.
# The *real* key is in your ".env" file.
SECRET_KEY = env("SECRET_KEY")

# We "outlaw" "slop" DEBUG in production.
DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = []  # This is "pro" for local. We will fix this for Railway.


# --- Application definition ---
# This is the "pro" order. Our "pro" apps go FIRST.
INSTALLED_APPS = [
    # "Pro" Apps
    "apps.users",
    "apps.portfolios",
    "apps.marketdata",
    "apps.calculators",
    "apps.analysis",
    # "Pro" 3rd-Party Apps
    "django_htmx",
    "allauth",
    "allauth.account",
    # "Slop" Apps (Django Defaults)
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",  # <--- "pro" allauth requirement
]

# This is the "pro" MIDDLEWARE block. It "outlaws" the "slop" error.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # THIS IS THE "PRO" FIX:
    "allauth.account.middleware.AccountMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "config.urls"

# This is the "pro" TEMPLATES block.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # This is the "pro" fix. We "outlaw" "slop" empty DIRS.
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# --- Database ---
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# --- Password validation ---
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# --- Internationalization ---
LANGUAGE_CODE = "en-gb"  # <--- This is "pro" for our "UK-First" app
TIME_ZONE = "UTC"
USE_I1N = True
USE_TZ = True


# --- Static files (CSS, JavaScript, Images) ---
STATIC_URL = "static/"


# --- Default primary key field type ---
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# --- "Pro" Custom User Model ---
AUTH_USER_MODEL = "users.CustomUser"

# --- "Pro" Auth (django-allauth) ---
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

SITE_ID = 1

LOGIN_REDIRECT_URL = "/dashboard/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/"

ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True

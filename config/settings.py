"""
Django settings for the Quantify "pro" project.
This is the "bulletproof," "non-slop" settings file.
"""

import environ
import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- "Pro" django-environ Setup ---
env = environ.Env()
# We silence the warning if .env is missing in production (Railway handles variables)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# --- "Pro" Security Keys ---
SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = ['*'] # For "basics-first" deployment.

# --- Application definition ---
INSTALLED_APPS = [
    # "Pro" Apps
    'apps.users',
    'apps.portfolios',
    'apps.marketdata',
    'apps.calculators',
    'apps.analysis',

    # "Pro" 3rd-Party Apps
    'django_htmx',
    'allauth',
    'allauth.account',
    'django_extensions',
    'django.contrib.humanize',
    
    # "Slop" Apps (Django Defaults)
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # "Pro" Static Files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'allauth.account.middleware.AccountMiddleware', # "Pro" Auth Middleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# --- Database ---
# "Pro" Database Switch (Postgres on Railway, SQLite locally)
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}


# --- Password validation ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# --- Internationalization ---
LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'UTC'
USE_I1N = True
USE_TZ = True


# --- Static files (WhiteNoise) ---
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# --- Default primary key field type ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- "Pro" Custom User Model ---
AUTH_USER_MODEL = 'users.CustomUser'

# --- "Pro" Auth (django-allauth) ---
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
SITE_ID = 1
LOGIN_REDIRECT_URL = '/dashboard/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

# --- "Pro" "Non-Slop" `allauth` Config ---
# We "outlaw" all "slop" warnings and "mediocre" settings.
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None

# "Pro" Fix: Using sets/lists correctly to silence warnings
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email']

# --- "Pro" Security (CSRF Fix) ---
# We "outlaw" the "slop" crash by adding https://
CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app', 
    'https://getquantify.co.uk',
    'https://www.getquantify.co.uk'
]
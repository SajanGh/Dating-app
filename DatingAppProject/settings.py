"""
Django settings for DatingAppProject project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv, find_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
load_dotenv(find_dotenv())
SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1","localhost"]


# Application definition

INSTALLED_APPS = [
"django.contrib.admin",
"django.contrib.auth",
"django.contrib.contenttypes",
"django.contrib.sessions",
"django.contrib.messages",
"django.contrib.staticfiles",
"django.contrib.sites",
#
# "allauth",
# "allauth.account",
# "allauth.socialaccount",
# "allauth.socialaccount.providers.google"
]
SITE_ID = 1
SOCIALACCOUNT_LOGIN_ON_GET = True


MY_APPS = [
"accounts.apps.AccountsConfig",
"user_profile.apps.UserProfileConfig",
"find_users.apps.FindUsersConfig",
"chat.apps.ChatConfig",
]

THIRD_PARTY_APPS = [
# Social Login Packages
"allauth",
"allauth.account",
"allauth.socialaccount",
"allauth.socialaccount.providers.google",
# Django Crispy Forms
"crispy_forms",
"crispy_bootstrap5",
# for cleaning old files and images after update
"django_cleanup",
# for notification system
"notifications",
# for real time chatting
"channels",
]

INSTALLED_APPS += MY_APPS + THIRD_PARTY_APPS

# Social login settings
AUTHENTICATION_BACKENDS = [
"django.contrib.auth.backends.ModelBackend",
"allauth.account.auth_backends.AuthenticationBackend",
]

SITE_ID = 1
LOGIN_URL = "account_login"
LOGIN_REDIRECT_URL = "index"
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_LOGOUT_ON_GET = True

SOCIALACCOUNT_PROVIDERS = {
"google": {
"SCOPE": [
"profile",
"email",
],
"AUTH_PARAMS": {
"access_type": "online",
},
}
}

MIDDLEWARE = [
"django.middleware.security.SecurityMiddleware",
"django.contrib.sessions.middleware.SessionMiddleware",
"django.middleware.common.CommonMiddleware",
"django.middleware.csrf.CsrfViewMiddleware",
"django.contrib.auth.middleware.AuthenticationMiddleware",
"django.contrib.messages.middleware.MessageMiddleware",
"django.middleware.clickjacking.XFrameOptionsMiddleware",

]

ROOT_URLCONF = "DatingAppProject.urls"

TEMPLATES = [
{
"BACKEND": "django.template.backends.django.DjangoTemplates",
"DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "DatingAppProject.wsgi.application"
ASGI_APPLICATION = "DatingAppProject.routing.application"
CHANNEL_LAYERS = {
"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"},
}

AUTH_USER_MODEL = "accounts.User"

FILTERS_EMPTY_CHOICE_LABEL = None

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
"default": {
"ENGINE": "django.db.backends.sqlite3",
"NAME": BASE_DIR / "db.sqlite3",
}
# "default": {
# "ENGINE": "django.db.backends.postgresql",
# "NAME": "datingapp",
# "USER": "postgres",
# "PASSWORD": "postgres",
# "HOST": "localhost",
# "PORT": "",
# }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kathmandu"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
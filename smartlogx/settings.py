"""
Django settings for smartlogx project.
"""
from pathlib import Path
import os
from decouple import config
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default="django-insecure-#aw=i#$zs6f=md95z4uu=x+l)=0!8a-t&#q4^p$awb0y&-*_d)")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['*', '.railway.app', 'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts",
    "logs",
    "adminpanel",
    "userpanel",
    # "public",  # Landing page disabled - direct to login
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

ROOT_URLCONF = "smartlogx.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = "smartlogx.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Database - Use PostgreSQL for production
DATABASE_URL = config('DATABASE_URL', default=None)
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    # Fallback to MySQL for local development
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": "smartlogx_db",
            "USER": "root",
            "PASSWORD": "root",
            "HOST": "localhost",
            "PORT": "3306",
            "OPTIONS": {
                "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
                "charset": "utf8mb4",
            },
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# For Vercel - disable static file serving
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Login URLs
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/logs/dashboard/'
LOGOUT_REDIRECT_URL = '/accounts/login/'


# ============================================
# EMAIL CONFIGURATION
# ============================================
# Configure these settings for sending welcome emails
# when admin creates new users in the system.
#
# For Gmail SMTP:
#   EMAIL_HOST = 'smtp.gmail.com'
#   EMAIL_PORT = 587
#   EMAIL_USE_TLS = True
#   EMAIL_HOST_USER = 'your-email@gmail.com'
#   EMAIL_HOST_PASSWORD = 'your-app-password'  # Use App Password, not regular password
#
# For Outlook/Office365:
#   EMAIL_HOST = 'smtp.office365.com'
#   EMAIL_PORT = 587
#   EMAIL_USE_TLS = True
#
# For custom SMTP server:
#   EMAIL_HOST = 'mail.yourdomain.com'
#   EMAIL_PORT = 587 or 465
#   EMAIL_USE_TLS = True (for port 587) or EMAIL_USE_SSL = True (for port 465)
# ============================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Change to your SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='pandikumar652001@gmail.com')  # Your sender email address
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='ljaq lzil dcxn dfmt')  # Your email password or app-specific password
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Admin email for receiving user notifications (Leave, WFH, Comp-Off, Log submissions)
# Can also be set via environment variable: os.environ.get('ADMIN_EMAIL', 'admin@teslead.com')
ADMIN_EMAIL = config('ADMIN_EMAIL', default='pandikumar652001@gmail.com')

# For development/testing, you can use console backend to see emails in terminal:
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


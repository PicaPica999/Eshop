"""
Django settings for Eshop project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-18-o085q31(gte=k^(jds8^x4x5qrm8gm#pa)yi^j7&k*tr*a('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mydemo',
    'captcha',
    'ckeditor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Eshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Eshop.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'CHARSET': 'utf8',
        'NAME': 'Eshop',
        'USER': 'root',
        'PASSWORD': 'xzz1045189077',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'pikapika_999@163.com'
EMAIL_HOST_PASSWORD = 'GNDAUGKAFXCWVGCM'
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

CAPTCHA_IMAGE_SIZE = (80, 45)
CAPTCHA_LENGTH = 4
CAPTCHA_TIMEOUT = 60
CAPTCHA_OUTPUT_FORMAT = '%(image)s %(text_field)s %(hidden_field)s '
CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_null',
                           'captcha.helpers.noise_arcs',
                           'captcha.helpers.noise_dots',
                           )
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge'

X_FRAME_OPTIONS = 'SAMEORIGIN'
CKEDITOR_UPLOAD_PATH = 'ckeditor_upload'
CKEDITOR_CONFIGS = {
    'default': {
        'width': 'auto',
        'height': '300px',
        'tabSpaces': 4,
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Preview', 'Smiley'],
            ['Bold', 'Italic', 'Underline', 'RemoveFormat', 'Blockquote'],
            ['TextColor', 'BGColor'],
            ['Format', 'Font', 'FontSize'],
            ['Link', 'Unlink'],
            ['Image', 'NumberedList', 'BulletedList'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Maximize']
        ],
        'extraPlugins': ','.join(['codesnippet', 'image2', 'filebrowser', 'widget', 'lineutils']),
    },
    'comment': {
        'width': 'auto',
        'height': '140px',
        'tabSpaces': 4,
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Smiley', 'CodeSnippet'],
            ['Bold', 'Italic', 'Underline', 'RemoveFormat', 'Blockquote'],
            ['TextColor', 'BGColor'],
            ['Link', 'Unlink'],
            ['NumberedList', 'BulletedList'],
        ],
        'extraPlugins': ','.join(['codesnippet']),
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

LOGIN_URL = '/login/'


LANGUAGE_CODE = 'zh-hans'
SIMPLEUI_HOME_INFO = False
SIMPLEUI_ANALYSIS = False

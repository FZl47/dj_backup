"""
 using Django 4.2.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-=e65traxe&q$)glc@3!ar9)cl_9z#*k^67k)=l7z3l0n(op%dc'

DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Apps
    'dj_backup',
    'django_q'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


LANGUAGE_CODE = 'fa-ir'

LANGUAGES = (
    ('fa', 'Persian'),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
MEDIA_URL = 'media/'

# STATIC_ROOT = BASE_DIR / 'static'
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static/'),
    os.path.join(BASE_DIR, 'dj_backup/static/'),
)


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

Q_CLUSTER = {
    'name': 'django-q',
    'orm': 'default',
    'retries': 3,
}

# DJ backup
DJ_BACKUP_CONFIG = {
    'POSTGRESQL_DUMP_PATH': None,  # optional(If the postgresql dump file is not found, you can set it)
    'MYSQL_DUMP_PATH': None,  # optional(If the mysql dump file is not found, you can set it)
    'EXTERNAL_DATABASES': {
        'external_db_1': {
            'ENGINE': 'xxx',
            'NAME': 'xxx',
            'USER': 'xxx',
            'PASSWORD': 'xxx',
            'HOST': '127.0.0.1',  # Or an IP Address that your DB is hosted on
        },
    },
    'BASE_ROOT_DIRS': [
        BASE_DIR,
    ],
    'BACKUP_TEMP_DIR': BASE_DIR / 'backup/temp',
    'STORAGES': {
        'LOCAL': {
            'OUT': BASE_DIR / 'backup/result'
        },
        'SFTP_SERVER': {
            'HOST': 'xxx.xxx.xxx.xxx',
            'USERNAME': 'xxx',
            'PASSWORD': 'xxx',
            'OUT': '/home/test_dj_backup/'
        },
        'FTP_SERVER': {
            'HOST': "xxx.xxx.xxx.xxx",
            'USERNAME': "xxx",
            'PASSWORD': "xxx",
            'OUT': '/test_dj_backup/'
        },
        'DROPBOX': {
            'ACCESS_TOKEN': 'xxx-xxx-xxx-..',
            'OUT': '/dj_backup/'
        }
    }
}


LOCALE_PATHS = (
    BASE_DIR / 'dj_backup/locale',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR.parent / 'logs/server.log',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

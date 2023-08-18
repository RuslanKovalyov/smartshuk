from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import os
from django.utils.translation import gettext_lazy as _

VALID_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'heic']
DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 20 #MB

BASE_DIR = Path(__file__).resolve().parent.parent

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

load_dotenv(find_dotenv())
SECRET_KEY = os.environ['SECRET_KEY']
 
DEV_MODE = True
DEBUG = True

#for map_popup shown in iframe
X_FRAME_OPTIONS = 'SAMEORIGIN'





# if DEV_MODE:
#     CACHE_TTL = 0
# else:
CACHE_TTL = 10 # seconds
CACHE_TTL_LEAFLET_MAP = 60 * 60 * 24 * 10 # 10days


ALLOWED_HOSTS = ['localhost', 'smartshuk.co.il', 'www.smartshuk.co.il', 'dev.smartshuk.co.il']

CSRF_TRUSTED_ORIGINS = ['http://localhost', 'https://smartshuk.co.il', 'https://www.smartshuk.co.il' , 'https://dev.smartshuk.co.il']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main.apps.MainConfig',
    'user.apps.UserConfig',
    'user_ads.apps.UserAdsConfig',
    'storages', #'storages', *It's not necessary. This library is not technically a django app.
    'captcha',
    'mapping_app',
    'honeypot',
]

# Google reCAPTCHA 
RECAPTCHA_PUBLIC_KEY = os.environ['RECAPTCHA_PUBLIC_KEY']
RECAPTCHA_PRIVATE_KEY = os.environ['RECAPTCHA_PRIVATE_KEY']
RECAPTCHA_VERSION = os.environ['RECAPTCHA_VERSION']
ENABLE_RECAPTCHA = not DEV_MODE

#For Use Custom User model in this case (username as email etc. )
# AUTH_USER_MODEL = 'AppName.ClassName'
AUTH_USER_MODEL = 'user.CustomUser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'smartshuk.urls'

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

WSGI_APPLICATION = 'smartshuk.wsgi.application'

# Database
if DEV_MODE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': os.environ['DB_ENGINE'],
            'NAME': os.environ['DB_NAME'],
            'USER': os.environ['DB_USER'],
            'PASSWORD': os.environ['DB_PASSWORD'],
            'HOST': os.environ['DB_HOST'],
            'PORT': os.environ['DB_PORT'],
        }
    }

#Caching
if DEV_MODE:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': os.path.join(BASE_DIR, 'cache/'), 
                    # for windows users: 'c:/path/to/django_cache'
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/1",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient"
            },
            "KEY_PREFIX": "smartshuk"
        }
    }

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


#LANGUAGE_CODE = 'en-us'
#LANGUAGE_CODE = 'ru'
LANGUAGE_CODE = 'he'

LANGUAGES = [
    ('he', _('Hebrew')),
    ('en', _('English')),
    # Add other languages here if needed
]


USE_I18N = True
USE_L10N = True

TIME_ZONE = 'Israel'
USE_TZ = True

# Static & Media files (CSS, JavaScript, Images, User-Dounloads etc.)
if DEV_MODE:
    STATIC_URL = 'static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

    MEDIA_URL = 'media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
else:
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
    AWS_DEFAULT_ACL = None
    AWS_S3_CUSTOM_DOMAIN = os.environ['AWS_S3_CUSTOM_DOMAIN']

    # AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',#1 day
    # 'ContentEncoding': 'gzip'
    }

    AWS_LOCATION = os.environ['AWS_LOCATION']
    AWS_STATIC_LOCATION = f'{AWS_LOCATION}/static'
    AWS_MEDIA_LOCATION = f'{AWS_LOCATION}/media'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_STATIC_LOCATION}/'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_MEDIA_LOCATION}/'

    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/login/'

def str_to_bool(value: str) -> bool:
    return value.lower() == 'true'
    
# Email settings
if DEV_MODE:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_ADDRESS = os.environ['EMAIL_ADDRESS']
    DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']
    EMAIL_BACKEND = os.environ['EMAIL_BACKEND']
    EMAIL_HOST = os.environ['EMAIL_HOST']
    EMAIL_PORT = os.environ['EMAIL_PORT']
    EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
    EMAIL_USE_TLS = str_to_bool( os.environ['EMAIL_USE_TLS'] )


'''
Deployment checklist

0 (optional) Clean up different types of data.

    python3 manage.py flush --noinput # This command will delete all data from the database, including data that is created by migrations.
    python3 manage.py clearsessions # This command will delete all data from the session table.
    python3 manage.py clearcache # This command will delete all data from the cache table.

    python3 manage.py migrate --fake app_name zero # Reset the migration history for the app in the database.
    
    find . -type f -name "0*.py*" -delete       # This command will delete all migration files.
    find . -type d -name "__pycache__" -exec rm -r {} +     # This command will delete all __pycache__ directories.

    clean static manually before collectstatic
    clean media manually

    rm db.sqlite3

    for dev mode:
        python3 manage.py makemigrations 
        python3 manage.py migrate
        python3 manage.py createsuperuser
        python3 manage.py runserver

1. Set DEBUG to False in your settings.
2. Configure production environment settings, like storage backend, database, caching, and email settings.
3. Run python3 manage.py makemigrations / migrate # python3 manage.py makemigrations # This command will create new migration files and apply the existing migrations to the new PostgreSQL database.
4. Run python3 manage.py collectstatic to collect static files into the proper storage backend.
5. Run python3 manage.py createsuperuser # This command will create a new superuser account.
6. Test application by running python3 manage.py runserver.
'''
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'honeypot_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'honeypot/honeypot.log'),
        },
    },
    'loggers': {
        # 'django': {
        #     'handlers': ['honeypot_file'],
        # },

        'honeypot': {
            'handlers': ['honeypot_file'],
            'level': 'DEBUG',
        },
    },
}


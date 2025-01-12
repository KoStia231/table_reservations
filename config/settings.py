import os
from datetime import timedelta
from pathlib import Path

from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env.prod')  # для docker .env.prod без docker .env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

DEBUG = os.getenv('DJANGO_DEBUG', False).lower() == 'true'

ALLOWED_HOSTS = [host.strip() for host in os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',') if host.strip()]
if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_DOMAIN = ALLOWED_HOSTS[0]
    CSRF_COOKIE_DOMAIN = ALLOWED_HOSTS[0]
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True
    SESSION_COOKIE_AGE = 3600

MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_ROOT = '/var/www/media/'

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = '/var/www/static/'

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

# ----------------------------------------------- Application definition -----------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'users',
    "main",
    "table_rezerv",

]

# ----------------------------------------------------- MIDDLEWARE -----------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ----------------------------------------------------- TEMPLATES ------------------------------------------------------
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

                'main.utils.context_processors.site_title',
            ],
        },
    },
]

# ---------------------------------------------- AUTH_PASSWORD_VALIDATORS ----------------------------------------------
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

# ---------------------------------------------- База данных PostgreSQL -----------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
    }
}

# -------------------------------------------------- Сервер для кеша ---------------------------------------------------
CACHES_ENABLED = os.getenv('DJANGO_CACHES_ENABLED', False).lower() == 'true'
if CACHES_ENABLED:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": os.getenv('REDIS_LOCATION'),
        }
    }

# -------------------------------------------- Настройки для аутентификации --------------------------------------------
AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# -------------------------------------- Настройки для почтового сервиса яндекса ---------------------------------------
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')  # Почта
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')  # Пароль приложения отправки
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', False).lower() == 'true'
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', False).lower() == 'true'

# -------------------------------------------- Настройки почтового сервера ---------------------------------------------
EMAIL_CONSOLE = os.getenv('EMAIL_CONSOLE', False).lower() == 'true'
if EMAIL_CONSOLE:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ------------------------------------------------ Настройки для Celery ------------------------------------------------
# URL-адрес брокера сообщений
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')  # Например, Redis, который по умолчанию работает на порту 6379
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')  # URL-адрес брокера результатов, также Redis
CELERY_TIMEZONE = os.getenv('CELERY_TIMEZONE')
CELERY_TASK_TRACK_STARTED = os.getenv('CELERY_TASK_TRACK_STARTED', False).lower() == 'true'
CELERY_TASK_TIME_LIMIT = 300  # Максимальное время на выполнение задачи
CELERY_WORKER_CONCURRENCY = 1  # 1 воркер для слабого сервера
CELERY_WORKER_PREFETCH_MULTIPLIER = 1  # очередь на одного воркера

CELERY_BEAT_SCHEDULE = {
    'send-habit-reminders-every-minute': {
        'task': 'table_rezerv.tasks.check_reservations',
        'schedule': timedelta(seconds=300),
    },
}

# Запуск задач синхронно
CELERY_TASK_ALWAYS_EAGER = os.getenv('CELERY_TASK_ALWAYS_EAGER', False).lower() == 'true'
# Исключения будут пробрасываться
CELERY_EAGER_PROPAGATES_EXCEPTIONS = os.getenv('CELERY_EAGER_PROPAGATES_EXCEPTIONS', False).lower() == 'true'

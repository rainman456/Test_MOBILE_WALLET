#import environ
import logging
import logging.config

from pathlib import Path
from django.utils.log import DEFAULT_LOGGING
from datetime import timedelta


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
#env = environ.Env(DEBUG=(bool, False))
#environ.Env.read_env(BASE_DIR / '.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-w28xn9_7%3g)#5%ryms3yuzq1jj-9%^6u2g1&l&g)#od23)a%n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
#env('ALLOWED_HOSTS').split(' ')


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

SITE_ID = 2

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'django_countries',
    'phonenumber_field',
    'anymail',
    'djoser',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'drf_yasg',
    'drf_spectacular_sidecar',
    #'allauth',
    'elasticemailbackend',
    #'dj_rest_auth.registration',
    "corsheaders",
     #'openai',
]
   
LOCAL_APPS = [
    'apps.users.apps.UsersConfig',
    
]


ELASTICEMAIL_API_KEY='0874BEA82EA8EDB1D31D187442104450718D478B290V8B65FDE75A2B90EF8485139C8BEC2B7A7FCCFA5D9C30B303B008'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

    
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = [
    "https://*",
    "http://*",
]

CSRF_TRUSTED_ORIGINS = [
    "http://*",
    "https://*",
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    #'djoser.backends.TokenAuthenticationBackend',

    #'dj_rest_auth.backends.AuthenticationBackend',
]

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

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_L10N = True

USE_TZ = True

logger = logging.getLogger(__name__)

LOG_LEVEL = "INFO"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/staticfiles/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIR = []
MEDIA_URL = '/mediafiles/'
MEDIA_ROOT = BASE_DIR / 'mediafiles'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.UserProfile'
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        #'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',

        #'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    #'DEFAULT_SCHEMA_CLASS': 'drf_yasg.openapi.AutoSchema',
}
"""
SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': (
        'Bearer', 'JWT',
    ),
    #'ACCESS_TOKEN_LIFETIME': timedelta(minutes=120),
    #'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    #'SIGNING_KEY':[],
    #env('SIGNING_KEY'),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}
"""

DJOSER = {
    #'SITE_URL': 'https://2164-102-176-246-49.ngrok-free.app/',
    'LOGIN_FIELD': 'email',
    'USER_CREATE_PASSWORD_RETYPE': False,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': False,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION':  False,
    'SEND_CONFIRMATION_EMAIL': False,
    'PASSWORD_RESET_CONFIRM_URL': '',
    #'SET_PASSWORD_RETYPE': True,
    #'PASSWORD_RESET_CONFIRM_RETYPE': True,
    #'USERNAME_RESET_CONFIRM_URL': 'email/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'api/v1/auth/users/activate/',
    'SEND_ACTIVATION_EMAIL': False,
    'SERIALIZERS': {
        'user_create': 'apps.users.serializers.CreateUser',
        'user_login': 'apps.users.serializers.LoginSerializer',
        'current_user': 'apps.users.serializers.UserCurrent',   
        #'delete_user': 'djoser.serializers.UserDeleteSerializer',
        #'activate': 'apps.users.serializers.OTPActivate',
        'password_reset': 'apps.users.serializers.SendOTPPasswordReset',
        'password_reset_confirm': 'apps.users.serializers.PasswordResetConfirm',

    }
}
"""
ANYMAIL={

    "SENDINBLUE_API_KEY":"xsmtpsib-8f0351ee1f8cd9ef6fbcfe41e0963dfb6a9f734b667d390929b06ed89e9d2119-EFn5Is4gA1t6a9qb"
}

"""
SPECTACULAR_SETTINGS = {
    'TITTLE': 'Vail Wallet API  ',
    'DESCRIPTION': 'Endpoints for user registration ,login and authentication',
    'VERSION': '1.0.0',
    'SWAGGER_UI_DIST': 'SIDECAR',  # shorthand to use the sidecar instead
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
}

SWAGGER_SETTINGS = {
'DEFAULT_INFO': 'core.urls.api_info',
}
   
#OPEN_API_KEY = []
#env('OPEN_API_KEY')

#THIS IS THE LAST SETTING CONFIG FOR BASE DONT PUT ANYTHING AFTER IT 

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_BACKEND = 'elasticemail.backend.ElasticEmailBackend'
DEFAULT_FROM_EMAIL='michaelstone897.com@gmail.com'
EMAIL_HOST='smtp.elasticemail.com'
#EMAIL_FROM = ''
MAIL_HOST_USER ='michaelstone897.com@gmail.com'
EMAIL_HOST_USER_PASSWORD = 'A78187B038ED84B8D27B236AA79A27C81AC1'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_PORT = 2525
DOMAIN =[]
#env('DOMAIN')
SITE_NAME = ''
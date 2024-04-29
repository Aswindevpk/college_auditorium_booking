from .base import *


# with open("/home/iedc/Devagiri_campus/secret_key.txt") as f:
#     SECRET_KEY = f.read().strip()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-752na=oybg19q9=gtcglr+z)81%gog3hbu7+v6-6&a-!ijo2^v'

DEBUG = False

ALLOWED_HOSTS = []

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# MEDIA_ROOT =  os.path.join(BASE_DIR, 'media/')
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

#HTTP settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

SECURE_HSTS_SECONDS = 31536000 #1 year
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
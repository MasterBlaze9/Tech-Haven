"""
Django settings for projetofinalbdII_grupo27 project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# Com a tua estrutura, BASE_DIR aponta para: /opt/render/project/src/Application/projetofinalbdII_grupo27
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-1bapw#vf#7&!6)=u+zg8&f*wzex-_d1+l@@*62z_a1y)7s1_@w')

# SECURITY WARNING: don't run with debug turned on in production!
# No Render, adiciona uma Env Var DEBUG=False. Se não existir, assume True para testes.
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'client',
    'component',
    'equipment',
    'production',
    'supplier',
    'user',
    'warehouse'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Corrigido: adicionada a vírgula
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'projetofinalbdII_grupo27.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'projetofinalbdII_grupo27.wsgi.application'


# Database
MONGO_URI = os.environ.get(
    'MONGO_URI',
    'mongodb+srv://ruinunoss_db_user:3Ij2zQZN7deSXTIf@blaze-techhaven.efnylni.mongodb.net/'
)
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME', 'projetofinal')

DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'neondb',
        'USER': 'neondb_owner',
        'PASSWORD': 'npg_Cy4tefI2oKub',
        'HOST': 'ep-odd-feather-abpx89zv.eu-west-2.aws.neon.tech',
        'PORT': '5432',
        'OPTIONS': {
            'sslmode': 'require',
        },
    },
    "admin_psql": {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'neondb',
        'USER': 'neondb_owner',
        'PASSWORD': 'npg_Cy4tefI2oKub',
        'HOST': 'ep-odd-feather-abpx89zv.eu-west-2.aws.neon.tech',
        'PORT': '5432',
        'OPTIONS': {
            'sslmode': 'require',
        },
    },
    "mongodb": {
        'ENGINE': 'djongo',
        'NAME': MONGO_DB_NAME,
        'CLIENT': {
            'host': MONGO_URI
        }
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Onde estão os teus ficheiros estáticos de desenvolvimento
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Caminho ABSOLUTO para a produção (staticfiles)
# Isso garante que o Render encontre a pasta no sistema de ficheiros
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'staticfiles'))

# Configuração WhiteNoise para servir e comprimir ficheiros
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)
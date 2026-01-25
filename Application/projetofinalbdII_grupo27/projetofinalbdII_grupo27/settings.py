from pathlib import Path
import os

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent


# ======================
# SECURITY
# ======================

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-dev-only"
)


ALLOWED_HOSTS = ["*"]

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "projetofinalbdII_grupo27.settings"
)


# ======================
# APPLICATIONS
# ======================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "client",
    "component",
    "equipment",
    "production",
    "supplier",
    "user",
    "warehouse",
]


# ======================
# MIDDLEWARE
# ======================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ======================
# URLS / WSGI
# ======================

ROOT_URLCONF = "projetofinalbdII_grupo27.urls"

WSGI_APPLICATION = "projetofinalbdII_grupo27.wsgi.application"


# ======================
# TEMPLATES
# ======================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(BASE_DIR / "templates")],
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


# ======================
# DATABASES
# ======================

MONGO_URI = os.environ.get("MONGO_URI")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "projetofinal")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "neondb"),
        "USER": os.environ.get("POSTGRES_USER", "neondb_owner"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("POSTGRES_HOST"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        "OPTIONS": {
            "sslmode": "require",
        },
    },

    "mongodb": {
        "ENGINE": "djongo",
        "NAME": MONGO_DB_NAME,
        "CLIENT": {
            "host": MONGO_URI
        }
    }
}


# ======================
# STATIC FILES (RENDER)
# ======================

STATIC_URL = "/static/"

# Render absolute path
STATIC_ROOT = "/opt/render/project/src/staticfiles"

# Local development static folder
STATICFILES_DIRS = [
    str(BASE_DIR / "static"),
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# ======================
# AUTH
# ======================

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
)


# ======================
# DEFAULTS
# ======================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

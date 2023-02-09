import os
from pathlib import Path
from utils.environment import convert_str_to_list

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.environ.get("DEBUG") == '0' else False

ALLOWED_HOSTS: list[str] = convert_str_to_list('ALLOWED_HOSTS')

CSRF_TRUSTED_ORIGINS: list[str] = convert_str_to_list('CSRF_TRUSTED_ORIGINS')

ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

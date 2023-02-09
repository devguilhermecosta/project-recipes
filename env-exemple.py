# Default objects per page
PER_PAGE = 9

# Default objects per page in dashboard
PER_PAGE_USER = 6

# Secret-Key for Django
SECRET_KEY = ''

# 0 = True, 1 = False
DEBUG = 0

# list of hosts
ALLOWED_HOSTS = ""

# Used for set the unsafe subdomain
CSRF_TRUSTED_ORIGINS = ''

# 1 = True, 0 = False
SELENIUM_HEADLESS = 1

# ------ DATABASE SETTINGS ------
# FROM SQLite
DATABASE_ENGINE = 'django.db.backends.sqlite3'
DATABASE_NAME = './db.sqlite3'

# FROM Postgres
# DATABASE_ENGINE = 'django.db.beckends.postgresql'
# DATABASE_NAME = 'database'
# DATABASE_USER = 'user'
# DATABASE_PASSWORD = 'password'
# DATABASE_HOST = 'host'
# DATABASE_PORT = 'port'

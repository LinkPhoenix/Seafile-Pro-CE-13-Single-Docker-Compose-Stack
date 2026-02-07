# -*- coding: utf-8 -*-
# Seahub configuration - Seafile Pro 13
# Example: example.com | SeaDoc (no Collabora) | No ClamAV, no Elasticsearch

import os

SECRET_KEY = 'your-secret-key-change-in-production'

# ---------------------------------------------------------------------------
# Security - cookies and hosts (HTTPS via Traefik)
# ---------------------------------------------------------------------------
##########################################################################
################ IMPORTANT: UPDATE THIS WITH YOUR DOMAIN #################
##########################################################################
# Include 127.0.0.1 / localhost / seafile for Docker healthcheck and internal calls
# (otherwise curl http://127.0.0.1:8000/api2/ping/ returns 400 and container stays unhealthy)
##########################################################################
################ IMPORTANT: UPDATE THIS WITH YOUR DOMAIN #################
##########################################################################
ALLOWED_HOSTS = [
    '.example.com',
    '.seafile.example.com',
    'seafile.example.com',
    '127.0.0.1',
    'localhost',
    'seafile',  # container name (internal calls)
]

# Secure cookies (HTTPS)
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'Strict'
CSRF_TRUSTED_ORIGINS = ['https://seafile.example.com']

# Session
SESSION_COOKIE_AGE = 60 * 60 * 24 * 14  # 2 weeks
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = False

# ---------------------------------------------------------------------------
# Email - e.g. mail.example.com:587
# ---------------------------------------------------------------------------
EMAIL_USE_TLS = True
EMAIL_HOST = 'mail.example.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'noreply@example.com'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

# ---------------------------------------------------------------------------
# WebDAV - enabled with secret (min length 16, strong level)
# ---------------------------------------------------------------------------
ENABLE_WEBDAV_SECRET = True
WEBDAV_SECRET_MIN_LENGTH = 16
WEBDAV_SECRET_STRENGTH_LEVEL = 3  # 3 = at least 3 types (digit, upper, lower, symbol)

# ---------------------------------------------------------------------------
# Two-factor authentication (2FA)
# ---------------------------------------------------------------------------
ENABLE_TWO_FACTOR_AUTH = True
# Optional: force 2FA for all users (uncomment if needed)
# ENABLE_FORCE_2FA_TO_ALL_USERS = True

# ---------------------------------------------------------------------------
# User settings
# ---------------------------------------------------------------------------
LOGIN_REMEMBER_DAYS = 7
ENABLE_CHANGE_PASSWORD = True
FORCE_PASSWORD_CHANGE = False

# ---------------------------------------------------------------------------
# General
# ---------------------------------------------------------------------------
TIME_ZONE = 'Europe/Paris'
LANGUAGE_CODE = 'en'
SITE_NAME = 'Seafile Pro'
SITE_TITLE = 'Seafile Pro'

# SeaDoc (no Collabora) - Wiki enabled
ENABLE_WIKI = True

# No virus scan (no ClamAV) - disabled explicitly
# ENABLE_UPLOAD_LINK_VIRUS_CHECK = False  # default False
# No check_virus_on_web_upload in seafile.conf

# Optional settings
ENABLE_SIGNUP = False
ACTIVATE_AFTER_REGISTRATION = False
NOTIFY_ADMIN_AFTER_REGISTRATION = True
SEND_EMAIL_ON_ADDING_SYSTEM_MEMBER = True
SEND_EMAIL_ON_RESETTING_USER_PASSWD = True
ENABLE_SETTINGS_VIA_WEB = True

MAX_NUMBER_OF_FILES_FOR_FILEUPLOAD = 500

# -*- coding: utf-8 -*-
# Seahub configuration - Seafile Community Edition 13
# Example: HTTPS via Traefik, no SeaDoc, no Collabora

import os

SECRET_KEY = 'your-secret-key-change-in-production'

# ---------------------------------------------------------------------------
# Security - cookies and hosts (HTTPS via Traefik)
# ---------------------------------------------------------------------------
ALLOWED_HOSTS = [
    '.example.com',
    '.seafile.example.com',
    'seafile.example.com',
    '127.0.0.1',
    'localhost',
    'seafile-ce',
]

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'Strict'
CSRF_TRUSTED_ORIGINS = ['https://seafile.example.com']

SESSION_COOKIE_AGE = 60 * 60 * 24 * 14
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = False

# ---------------------------------------------------------------------------
# Email
# ---------------------------------------------------------------------------
EMAIL_USE_TLS = True
EMAIL_HOST = 'mail.example.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'noreply@example.com'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

# ---------------------------------------------------------------------------
# WebDAV
# ---------------------------------------------------------------------------
ENABLE_WEBDAV_SECRET = True
WEBDAV_SECRET_MIN_LENGTH = 16
WEBDAV_SECRET_STRENGTH_LEVEL = 3

# ---------------------------------------------------------------------------
# Two-factor authentication
# ---------------------------------------------------------------------------
ENABLE_TWO_FACTOR_AUTH = True

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
SITE_NAME = 'Seafile'
SITE_TITLE = 'Seafile'

# CE: no SeaDoc, no ENABLE_WIKI (or set True if you add SeaDoc later)
# ENABLE_WIKI = False

# Optional
ENABLE_SIGNUP = False
ACTIVATE_AFTER_REGISTRATION = False
NOTIFY_ADMIN_AFTER_REGISTRATION = True
SEND_EMAIL_ON_ADDING_SYSTEM_MEMBER = True
SEND_EMAIL_ON_RESETTING_USER_PASSWD = True
ENABLE_SETTINGS_VIA_WEB = True

MAX_NUMBER_OF_FILES_FOR_FILEUPLOAD = 500

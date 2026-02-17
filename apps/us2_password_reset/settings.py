from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
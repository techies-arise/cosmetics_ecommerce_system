# import os
# import dj_database_url  # Common utility to parse production DB URIs
# from .base import *

# # 1. Turn off debug mode completely
# DEBUG = False

# # 2. Restrict access to your live domain names only
# ALLOWED_HOSTS = [
#     'yourdomain.com',
#     '://yourdomain.com',
# ]

# # 3. Pull your critical secret key from live environment variables
# SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# # 4. Connect to your robust production database
# DATABASES = {
#     'default': dj_database_url.config(
#         default=os.environ.get('DATABASE_URL'),
#         conn_max_age=600,  # Keeps database connections alive for performance
#     )
# }

# # 5. Enforce strict HTTPS/SSL security rules
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_HSTS_SECONDS = 31536000  # Forces HTTPS for 1 year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

# # 6. Route emails through a real delivery service provider
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = os.environ.get('EMAIL_HOST')
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

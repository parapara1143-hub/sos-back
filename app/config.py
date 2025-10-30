import os

import os
from datetime import timedelta
class Config:

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL","sqlite:///sos.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY","dev-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY","dev-jwt")
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS","*")
    DEFAULT_RATE_LIMIT = os.getenv("DEFAULT_RATE_LIMIT","200/hour")
    FCM_SERVER_KEY = os.getenv("FCM_SERVER_KEY")
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    SENDGRID_FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL","no-reply@sos.local")
    GRAYLOG_HTTP_ENDPOINT = os.getenv("GRAYLOG_HTTP_ENDPOINT")
    DATADOG_HTTP_ENDPOINT = os.getenv("DATADOG_HTTP_ENDPOINT")
    ENABLE_PUBLIC_API_KEYS = os.getenv("ENABLE_PUBLIC_API_KEYS","false").lower()=="true"
    INTEGRATION_SECRET = os.getenv("INTEGRATION_SECRET","change-this-secret")


# JWT expirations
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv("JWT_ACCESS_MINUTES","15")))
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv("JWT_REFRESH_DAYS","30")))
# Storage
STORAGE_PROVIDER = os.getenv("STORAGE_PROVIDER","local")  # local or s3
STORAGE_LOCAL_DIR = os.getenv("STORAGE_LOCAL_DIR","uploads")
STORAGE_BASE_URL = os.getenv("STORAGE_BASE_URL","/files")  # if local, served by app
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
AWS_REGION = os.getenv("AWS_REGION","us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

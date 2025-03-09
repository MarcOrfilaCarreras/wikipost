import os

from dotenv import load_dotenv


class Config:
    load_dotenv('.env')

    API_DATABASE_FILE = os.getenv('API_DATABASE_FILE', 'db.sqlite')
    API_JWT_TOKEN = os.getenv('API_JWT_TOKEN', None)

    API_REDIS_HOST = os.getenv('API_REDIS_HOST', '')
    API_REDIS_PORT = os.getenv('API_REDIS_PORT', '')
    API_REDIS_DB = os.getenv('API_REDIS_DB', 0)

    API_ENCRYPTION_KEY = os.getenv('API_ENCRYPTION_KEY', '')

    API_SENTRY = os.getenv('API_SENTRY', '')

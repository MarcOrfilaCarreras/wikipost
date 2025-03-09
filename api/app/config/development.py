from .base import Config


class DevelopmentConfig(Config):
    DEBUG = True

    HOST = '127.0.0.1'
    PORT = '8080'

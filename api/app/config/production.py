from .base import Config


class ProductionConfig(Config):
    DEBUG = False

    HOST = '0.0.0.0'
    PORT = '8080'

import os

import sentry_sdk
from flask import Flask

from .config.development import DevelopmentConfig
from .config.production import ProductionConfig
from .db.connector import DatabaseConnector
from .db.migrator import DatabaseMigrator
from .extensions import encryption
from .extensions import scheduler
from .external.instagram import ProxyManager
from .middleware.cors import cors
from .middleware.requests import requests_logging
from .utils.encrypt import Encryption
from .utils.jwt import JWTManager
from .utils.routes import register_blueprints
from .utils.scheduler import Scheduler


def create_app():
    app = Flask(__name__)
    env = os.environ.get('API_ENVIRONMENT', 'development')

    if env == 'production':
        app.config.from_object(ProductionConfig)

        sentry_sdk.init(
            dsn=app.config.get('API_SENTRY'),
            send_default_pii=True,
            traces_sample_rate=1.0,
        )
    elif env == 'development':
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    register_blueprints(app=app, path='./app/routes')
    requests_logging(app=app)
    cors(app=app)

    db_connector = DatabaseConnector(app.config.get('API_DATABASE_FILE'))

    db_migrator = DatabaseMigrator()
    db_migrator.migrate()

    JWTManager.set_secret(secret=app.config.get('API_JWT_TOKEN'))

    encryption = Encryption(key=app.config.get('API_ENCRYPTION_KEY'))

    scheduler = Scheduler(redis_host=app.config.get('API_REDIS_HOST'), redis_port=app.config.get(
            'API_REDIS_PORT'), redis_db=app.config.get('API_REDIS_DB'))
    scheduler.connect()
    scheduler.start()

    proxy_manager = ProxyManager()

    return app

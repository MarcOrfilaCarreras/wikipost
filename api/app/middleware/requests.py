import time

from flask import g
from flask import request

from ..extensions import logging


def requests_logging(*, app=None):
    @app.before_request
    def log_request():
        g.start_time = time.time()

    @app.after_request
    def log_response(response):
        duration = time.time() - g.start_time
        logging.info(
            f'[REQUEST] {request.url} {request.method} {response.status_code} {duration:.4f} seconds')
        return response

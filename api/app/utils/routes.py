import importlib
import os
import sys
from datetime import datetime
from datetime import timedelta
from functools import wraps

from app.extensions import logging
from app.utils.jwt import JWTManager
from flask import abort
from flask import request


def register_blueprints(*, app=None, path=None):
    if app is None:
        raise ValueError('app argument must be specified')

    if path is None:
        raise ValueError('path argument must be specified')

    base_path = os.path.abspath(path)
    sys.path.insert(0, base_path)

    logging.info(
        f'[BLUEPRINTS] Starting to register blueprints from path: {base_path}')

    for root, dirs, files in os.walk(base_path):
        relative_root = os.path.relpath(root, base_path)

        for file in files:
            if file.endswith('.py'):
                blueprint_name = f"{relative_root.replace(os.sep, '.')}.{file[:-3]}"

                if blueprint_name.startswith('.'):
                    blueprint_name = blueprint_name[1:]

                try:
                    logging.info(
                        f'[BLUEPRINTS] Attempting to import blueprint: {blueprint_name}')
                    blueprint = importlib.import_module(blueprint_name)

                    if hasattr(blueprint, 'register'):
                        blueprint.register(app=app)
                        logging.info(
                            f'[BLUEPRINTS] Successfully registered blueprint: {blueprint_name}')
                    else:
                        logging.warning(
                            f"[BLUEPRINTS] Blueprint {blueprint_name} does not have a 'register' function")

                except ModuleNotFoundError as e:
                    logging.error(
                        f'[BLUEPRINTS] Error importing blueprint: {blueprint_name} - {e}')
                    continue
                except Exception as e:
                    logging.error(
                        f'[BLUEPRINTS] Unexpected error while importing blueprint: {blueprint_name} - {e}')


def authorization_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        header = request.headers.get('Authorization')

        if (not header) or (len(header.split(' ')) <= 1) or (JWTManager.verify(header.split(' ')[1]) == False):
            abort(401)

        payload = JWTManager.decode(header.split(' ')[1])

        if datetime.now() > (datetime.fromtimestamp(payload['exp']) + timedelta(minutes=60)):
            abort(401)

        return func(*args, **kwargs)
    return decorated_function

from app.services.post import upload_post
from app.services.user import get_user_by_email
from app.services.user import get_user_jwt_token
from app.services.user import get_user_settings
from app.services.user import update_user_settings
from app.utils.scheduler import Scheduler
from app.utils.validation import valid_email
from app.utils.validation import valid_password
from flask import Blueprint
from flask import jsonify
from flask import request
from werkzeug.security import check_password_hash

blueprint = Blueprint('auth-login', __name__)


def post():
    data = request.json

    email = data.get('email')
    password = data.get('password')

    if (email is None) or (not valid_email(email)):
        return jsonify({'message': 'Invalid email format', 'status': 'fail'}), 400

    if (password is None) or (not valid_password(password)):
        return jsonify({'message': 'Password must be at least 12 characters long and include letters and numbers', 'status': 'fail'}), 400

    user = get_user_by_email(email=email)
    if not user:
        return jsonify({'message': 'User not found. Please check the email or try again later', 'status': 'fail'}), 400

    if not check_password_hash(user.password, password):
        return jsonify({'message': 'Incorrect password. Please check your credentials and try again', 'status': 'fail'}), 400

    settings = get_user_settings(user=user.id)
    if (settings is not None) and (settings.scheduler == '' or settings.scheduler is None):
        scheduler = Scheduler()
        job = scheduler.add_job(
            upload_post, settings.scheduler_interval, kwargs={'user': user.id})

        updated_data = {key: settings.to_dict().get(key, getattr(settings, key)) for key in settings.to_dict(
        ).keys() if not key.startswith('_') and (key not in ['id', 'created_at'])}
        updated_data['scheduler'] = job.id

        update_user_settings(user=user.id, **updated_data)

    return jsonify({'data': {'token': get_user_jwt_token(user=user)}, 'status': 'success'}), 200


blueprint.add_url_rule('/auth/login', view_func=post, methods=['POST'])


def register(app):
    app.register_blueprint(blueprint)

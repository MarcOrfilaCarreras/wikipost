from app.services.user import create_user
from app.services.user import create_user_settings
from app.utils.validation import valid_email
from app.utils.validation import valid_password
from flask import Blueprint
from flask import jsonify
from flask import request
from werkzeug.security import generate_password_hash

blueprint = Blueprint('auth-register', __name__)


def post():
    data = request.json

    email = data.get('email')
    password = data.get('password')

    if (email is None) or (not valid_email(email)):
        return jsonify({'message': 'Invalid email format', 'status': 'fail'}), 400

    if (password is None) or (not valid_password(password)):
        return jsonify({'message': 'Password must be at least 12 characters long and include letters and numbers', 'status': 'fail'}), 400

    password = generate_password_hash(password)

    user = create_user(email=email, password=password)
    if not user:
        return jsonify({'message': 'User could not be created. Please check the email or try again later', 'status': 'fail'}), 400

    settings = create_user_settings(
        user=user.id, ai_prompt='', scheduler_interval='0 0 * * *')
    if not settings:
        return jsonify({'message': 'User created without settings. You may need to contact support', 'status': 'fail'}), 400

    return jsonify({'data': user.to_dict(), 'status': 'success'}), 201


blueprint.add_url_rule('/auth/register', view_func=post, methods=['POST'])


def register(*, app=None):
    if app is None:
        raise ValueError('app argument must be specified')

    app.register_blueprint(blueprint)

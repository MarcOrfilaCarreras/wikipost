from app.extensions import encryption
from app.services.post import upload_post
from app.services.user import get_user_settings
from app.services.user import update_user_settings
from app.utils.jwt import JWTManager
from app.utils.routes import authorization_required
from app.utils.scheduler import Scheduler
from flask import abort
from flask import Blueprint
from flask import jsonify
from flask import request

blueprint = Blueprint('account-settings', __name__)


@authorization_required
def get():
    user = JWTManager.decode(request.headers.get(
        'Authorization').split(' ')[1])['id']

    if (user is None):
        abort(401)

    settings = get_user_settings(user=user)
    if settings is None:
        return jsonify({'data': None, 'status': 'fail'}), 400

    settings.instagram_password = encryption.decrypt(
        settings.instagram_password)

    settings.instagram_email_password = encryption.decrypt(
        settings.instagram_email_password)

    return jsonify({'data': settings.to_dict(), 'status': 'success'}), 200


@authorization_required
def post():
    data = request.json

    ai_prompt = data.get('ai_prompt')
    if ai_prompt is None:
        return jsonify({'message': 'You must provide the AI Prompt field', 'status': 'fail'}), 400

    user = JWTManager.decode(request.headers.get(
        'Authorization').split(' ')[1])['id']

    if (user is None):
        abort(401)

    settings = get_user_settings(user=user)
    if settings is None:
        return jsonify({'message': 'User settings not found.', 'status': 'fail'}), 400

    updated_data = {key: data.get(key, getattr(settings, key)) for key in settings.__dict__.keys(
    ) if not key.startswith('_') and (key not in ['id', 'created_at'])}

    if 'instagram_password' in updated_data.keys():
        updated_data['instagram_password'] = encryption.encrypt(
            updated_data['instagram_password'])

    if 'instagram_email_password' in updated_data.keys():
        updated_data['instagram_email_password'] = encryption.encrypt(
            updated_data['instagram_email_password'])

    if 'scheduler_interval' in updated_data.keys():
        scheduler = Scheduler()

        if not scheduler.delete_job(id=settings.scheduler):
            return jsonify({'message': 'Settings could not be updated.', 'status': 'fail'}), 400

        job = scheduler.add_job(
            upload_post, updated_data['scheduler_interval'], kwargs={'user': user})
        updated_data['scheduler'] = job.id

    updated_settings = update_user_settings(user=user, **updated_data)
    if not updated_settings:
        return jsonify({'message': 'Settings could not be updated.', 'status': 'fail'}), 400

    updated_settings.instagram_password = encryption.decrypt(
        updated_settings.instagram_password)

    updated_settings.instagram_email_password = encryption.decrypt(
        updated_settings.instagram_email_password)

    return jsonify({'data': updated_settings.to_dict(), 'status': 'success'}), 201


blueprint.add_url_rule('/account/settings', view_func=get, methods=['GET'])
blueprint.add_url_rule('/account/settings', view_func=post, methods=['POST'])


def register(app):
    app.register_blueprint(blueprint)

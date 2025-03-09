from app.services.post import delete_post
from app.services.post import get_post
from app.services.post import update_post
from app.utils.jwt import JWTManager
from app.utils.routes import authorization_required
from flask import abort
from flask import Blueprint
from flask import jsonify
from flask import request

blueprint = Blueprint('account-post', __name__)


@authorization_required
def post(post=None):
    data = request.json

    user = JWTManager.decode(request.headers.get(
        'Authorization').split(' ')[1])['id']

    if (user is None):
        abort(401)

    if (post is None):
        abort(404)

    post_ = get_post(id=post)
    if post_ is None:
        return jsonify({'message': 'Post not found.', 'status': 'fail'}), 400

    updated_data = {key: data.get(key, getattr(post_, key)) for key in post_.__dict__.keys(
    ) if not key.startswith('_') and (key not in ['id', 'created_at'])}

    updated_post = update_post(id=post, **updated_data)
    if not updated_post:
        return jsonify({'message': 'Post could not be updated.', 'status': 'fail'}), 400

    return jsonify({'data': updated_post.to_dict(), 'status': 'success'}), 200


@authorization_required
def delete(post=None):
    user = JWTManager.decode(request.headers.get(
        'Authorization').split(' ')[1])['id']

    if (user is None):
        abort(401)

    if (post is None):
        abort(404)

    if delete_post(id=post) is False:
        return jsonify({'data': None, 'status': 'fail'}), 400

    return jsonify({'data': None, 'status': 'success'}), 200


blueprint.add_url_rule('/account/posts/<post>',
                       view_func=post, methods=['POST'])
blueprint.add_url_rule('/account/posts/<post>',
                       view_func=delete, methods=['DELETE'])


def register(app):
    app.register_blueprint(blueprint)

from app.services.user import get_user_posts
from app.utils.jwt import JWTManager
from app.utils.routes import authorization_required
from flask import abort
from flask import Blueprint
from flask import jsonify
from flask import request

blueprint = Blueprint('account-posts', __name__)


@authorization_required
def get():
    user = JWTManager.decode(request.headers.get(
        'Authorization').split(' ')[1])['id']

    if (user is None):
        abort(401)

    allowed = request.args.get('allowed', type=str)
    if allowed is not None:
        allowed = allowed.lower() == 'true'
    else:
        allowed = None

    published = request.args.get('published', type=str)
    if published is not None:
        published = published.lower() == 'true'
    else:
        published = None

    posts = get_user_posts(user=user, allowed=allowed, published=published)
    if posts is None:
        return jsonify({'data': None, 'status': 'success'}), 200

    return jsonify({'data': [p.to_dict() for p in posts], 'status': 'success'}), 200


blueprint.add_url_rule('/account/posts', view_func=get, methods=['GET'])


def register(app):
    app.register_blueprint(blueprint)

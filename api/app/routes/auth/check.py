from app.utils.routes import authorization_required
from flask import Blueprint
from flask import jsonify
from flask import request


blueprint = Blueprint('auth-check', __name__)


@authorization_required
def get():
    return jsonify({'data': None, 'status': 'success'}), 200


blueprint.add_url_rule('/auth/check', view_func=get, methods=['GET'])


def register(app):
    app.register_blueprint(blueprint)

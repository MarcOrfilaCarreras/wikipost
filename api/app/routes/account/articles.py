from app.external.wikipedia import Scraper
from app.services.article import create_article
from app.services.user import get_user_articles
from app.utils.jwt import JWTManager
from app.utils.routes import authorization_required
from app.utils.validation import valid_url
from flask import abort
from flask import Blueprint
from flask import jsonify
from flask import request

blueprint = Blueprint('account-articles', __name__)


@authorization_required
def get():
    user = JWTManager.decode(request.headers.get(
        'Authorization').split(' ')[1])['id']

    if (user is None):
        abort(401)

    articles = get_user_articles(user=user)
    if articles is None:
        return jsonify({'data': None, 'status': 'fail'}), 200

    return jsonify({'data': [a.to_dict() for a in articles], 'status': 'success'}), 200


@authorization_required
def post():
    data = request.json

    url = data.get('url')
    user = JWTManager.decode(request.headers.get(
        'Authorization').split(' ')[1])['id']

    if (url is None) or (not valid_url(url)):
        return jsonify({'message': 'Invalid url format', 'status': 'fail'}), 400

    if (user is None):
        abort(401)

    try:
        scraper = Scraper()
        _, title, _, content = scraper.scrape(url=url)
    except Exception as e:
        return jsonify({'message': 'Article could not be created.', 'status': 'fail'}), 400

    article = create_article(user=user, title=title, content=content, url=url)
    if not article:
        return jsonify({'message': 'Article could not be created.', 'status': 'fail'}), 400

    return jsonify({'data': article.to_dict(), 'status': 'success'}), 201


blueprint.add_url_rule('/account/articles', view_func=get, methods=['GET'])
blueprint.add_url_rule('/account/articles', view_func=post, methods=['POST'])


def register(app):
    app.register_blueprint(blueprint)

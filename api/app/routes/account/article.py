import json
import random

from app.external.ai import LLM
from app.external.google import ImageDownloader
from app.external.wikipedia import Scraper
from app.services.article import delete_article
from app.services.article import get_article
from app.services.post import create_option
from app.services.post import create_post
from app.services.post import create_question
from app.services.user import get_user_settings
from app.utils.jwt import JWTManager
from app.utils.routes import authorization_required
from app.utils.validation import valid_url
from flask import abort
from flask import Blueprint
from flask import jsonify
from flask import request
from markdown_it import MarkdownIt
from mdit_plain.renderer import RendererPlain

blueprint = Blueprint('account-article', __name__)


@authorization_required
def get(article=None):
    user = JWTManager.decode(request.headers.get(
        'Authorization').split(' ')[1])['id']

    if (user is None):
        abort(401)

    if (article is None):
        abort(404)

    article = get_article(id=article)
    if article is None:
        return jsonify({'data': None, 'status': 'fail'}), 404

    return jsonify({'data': article.to_dict(), 'status': 'success'}), 200


@authorization_required
def delete(article=None):
    user = JWTManager.decode(request.headers.get(
        'Authorization').split(' ')[1])['id']

    if (user is None):
        abort(401)

    if (article is None):
        abort(404)

    deleted = delete_article(id=article)
    if deleted is False:
        return jsonify({'data': None, 'status': 'fail'}), 400

    return jsonify({'data': None, 'status': 'success'}), 200


@authorization_required
def generate(article=None):
    user = JWTManager.decode(request.headers.get(
        'Authorization').split(' ')[1])['id']

    if (user is None):
        abort(401)

    if (article is None):
        abort(404)

    article = get_article(id=article)
    if article is None:
        return jsonify({'data': 'You must provide the Article ID', 'status': 'fail'}), 400

    settings = get_user_settings(user=user)
    if settings is None:
        return jsonify({'data': 'User settings not found', 'status': 'fail'}), 400

    downloader = ImageDownloader()
    images = downloader.query(query=article.title)

    url = None
    if len(images) > 0:
        url = images[random.randint(0, 3 if len(images) > 4 else 0)]

    if url is None:
        return jsonify({'message': 'The image could not be found.', 'status': 'fail'}), 400

    message = f"""
    {settings.ai_prompt}

    {article.content}
    """

    llm = LLM()
    result = llm.query(message=message)
    result = result.replace('"', "'")

    parser = MarkdownIt(renderer_cls=RendererPlain)
    result = parser.render(result)

    post = create_post(user=user, content=result, url=url)
    if post is None:
        return jsonify({'message': 'Post could not be created.', 'status': 'fail'}), 400

    message = """
    Given the text below, generate one multiple-choice question in the same language as the text. The question should be based on the content of the text. Provide three answer options. Exactly one option should be marked correct using "correct": 1, and the others should be marked as incorrect with "correct": 0.

    Return the result strictly in the following JSON format:
    {
        "question": "",
        "options": [
            {"option": "", "correct": 0},
            {"option": "", "correct": 1},
            {"option": "", "correct": 0}
        ]
    }

    Use the following text to generate the question and options:\n
    """
    message = message + article.content

    result = llm.query(message=message)
    result = result.replace('"', "'")
    result = parser.render(result)
    result = result.replace("'", '"')

    result_parsed = json.loads(result)

    question = None
    if 'question' in result_parsed.keys():
        question = create_question(
            post=post.id, content=result_parsed['question'])

    if (question is not None) and ('options' in result_parsed.keys()):
        for option in result_parsed['options']:
            create_option(question=question.id,
                          content=option['option'], is_correct=option['correct'])

    return jsonify({'data': post.to_dict(), 'status': 'success'}), 200


blueprint.add_url_rule('/account/articles/<article>',
                       view_func=get, methods=['GET'])
blueprint.add_url_rule('/account/articles/<article>/generate',
                       view_func=generate, methods=['POST'])
blueprint.add_url_rule('/account/articles/<article>',
                       view_func=delete, methods=['DELETE'])


def register(app):
    app.register_blueprint(blueprint)

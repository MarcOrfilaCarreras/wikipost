from flask import jsonify


def register(*, app=None):
    if app is None:
        raise ValueError('app argument must be specified')

    @app.errorhandler(401)
    def not_authorized(message):
        return jsonify({
            'status': 'fail',
            'message': 'Not authorized'
        }), 401

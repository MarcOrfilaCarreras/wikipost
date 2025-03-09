from flask import jsonify


def register(*, app=None):
    if app is None:
        raise ValueError('app argument must be specified')

    @app.errorhandler(405)
    def method_not_allowed(message):
        return jsonify({
            'status': 'fail',
            'message': 'Method Not Allowed'
        }), 404

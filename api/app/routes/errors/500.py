from flask import jsonify


def register(*, app=None):
    if app is None:
        raise ValueError('app argument must be specified')

    @app.errorhandler(500)
    def internal_server_error(message):
        return jsonify({
            'status': 'fail',
            'message': 'An unexpected error occurred on the server. Please try again later.'
        }), 500

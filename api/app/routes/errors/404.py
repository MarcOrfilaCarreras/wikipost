from flask import jsonify


def register(*, app=None):
    if app is None:
        raise ValueError('app argument must be specified')

    @app.errorhandler(404)
    def not_found(message):
        return jsonify({
            'status': 'fail',
            'message': 'Resource not found'
        }), 404
